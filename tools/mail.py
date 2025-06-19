# -*- coding: utf-8 -*-
import email
import imaplib
from email.header import decode_header
import chardet
import re
import json
from bs4 import BeautifulSoup
import logging
from ticket.ticket_parser import parse_ticket_info, parse_refund_info, clean_text_content, validate_ticket_info
from ticket.models import TicketDB
from config import EMAIL_CONFIG, PASSENGER_FILTER, MAIL_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def remove_html_tags_and_whitespace(html_content):
    """
    去除HTML标签和空白字符
    :param html_content: HTML内容
    :return: str 清理后的文本
    """
    # 使用 BeautifulSoup 去除 HTML 标签
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    # 去除所有空格、换行符和制表符
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    return clean_text

class MailReader:
    def __init__(self, imap_host=None, email_user=None, email_pwd=None):
        """
        初始化邮件读取器
        :param imap_host: IMAP服务器地址
        :param email_user: 邮箱账号
        :param email_pwd: 邮箱密码
        """
        self.imap_host = imap_host or EMAIL_CONFIG["imap_host"]
        self.email_user = email_user or EMAIL_CONFIG["email_user"]
        self.email_pwd = email_pwd or EMAIL_CONFIG["email_pwd"]
        self.imap_client = None

    def connect(self):
        """
        连接到IMAP服务器
        """
        try:
            self.imap_client = imaplib.IMAP4(self.imap_host)
            logger.info(f"成功连接到 {self.imap_host}")
        except Exception as e:
            logger.error(f"连接IMAP服务器失败: {e}")
            raise

    def login(self):
        """
        登录邮箱
        """
        try:
            self.imap_client.login(self.email_user, self.email_pwd)
            imaplib.Commands["ID"] = ('AUTH',)
            args = ("name", self.email_user, "contact", self.email_user, "version", "1.0.0", "vendor", "myclient")
            self.imap_client._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))
            logger.info(f"成功登录邮箱: {self.email_user}")
        except Exception as e:
            logger.error(f"邮箱登录失败: {e}")
            raise

    def select_folder(self, folder_name=None):
        """
        选择邮件文件夹
        :param folder_name: 文件夹名称
        """
        folder_name = folder_name or EMAIL_CONFIG["folder_name"]
        try:
            self.imap_client.select(folder_name)
            logger.info(f"成功选择文件夹: {folder_name}")
        except Exception as e:
            logger.error(f"选择文件夹失败: {e}")
            raise

    def search_emails(self, search_criteria="ALL"):
        """
        搜索邮件
        :param search_criteria: 搜索条件
        :return: list 邮件ID列表
        """
        try:
            status, messages = self.imap_client.search(None, search_criteria)
            email_ids = messages[0].split()
            logger.info(f"找到 {len(email_ids)} 封邮件")
            return email_ids
        except Exception as e:
            logger.error(f"搜索邮件失败: {e}")
            return []

    def fetch_email_data(self, email_id):
        """
        获取邮件数据
        :param email_id: 邮件ID
        :return: email.message.Message 邮件对象
        """
        try:
            status, msg_data = self.imap_client.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    return msg
            return None
        except Exception as e:
            logger.error(f"获取邮件数据失败: {e}")
            return None

    def decode_header_field(self, header_value):
        """
        解码邮件头字段
        :param header_value: 邮件头值
        :return: str 解码后的值
        """
        if not header_value:
            return ""
        try:
            decoded_value, encoding = decode_header(header_value)[0]
            if isinstance(decoded_value, bytes):
                return decoded_value.decode(encoding if encoding else 'utf-8')
            return decoded_value
        except Exception as e:
            logger.error(f"解码邮件头失败: {e}")
            return str(header_value)

    def parse_email(self, email_id):
        """
        解析邮件内容
        :param email_id: 邮件ID
        :return: dict 解析后的邮件信息
        """
        msg = self.fetch_email_data(email_id)
        if msg is None:
            return None

        try:
            subject = self.decode_header_field(msg["subject"])
            sender = self.decode_header_field(msg["from"])
            date = msg['date']

            mail_content = ""
            html_content = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        payload = part.get_payload(decode=True)
                        detected_encoding = chardet.detect(payload)['encoding']
                        mail_content = payload.decode(detected_encoding, errors='ignore')
                    elif content_type == 'text/html':
                        payload = part.get_payload(decode=True)
                        detected_encoding = chardet.detect(payload)['encoding']
                        html_content = payload.decode(detected_encoding, errors='ignore')
            else:
                payload = msg.get_payload(decode=True)
                if msg.get_content_type() == 'text/plain':
                    detected_encoding = chardet.detect(payload)['encoding']
                    mail_content = payload.decode(detected_encoding, errors='ignore')
                elif msg.get_content_type() == 'text/html':
                    detected_encoding = chardet.detect(payload)['encoding']
                    html_content = payload.decode(detected_encoding, errors='ignore')

            # 去掉 HTML 标签
            final_content = remove_html_tags_and_whitespace(html_content) if html_content else mail_content

            return {
                'subject': subject,
                'from': sender,
                'date': date,
                'content': clean_text_content(final_content)
            }
        except Exception as e:
            logger.error(f"解析邮件失败: {e}")
            return None

    def read_emails(self, folder_name=None, max_emails=None):
        """
        读取邮件列表
        :param folder_name: 文件夹名称
        :param max_emails: 最大邮件数量
        :return: list 邮件信息列表
        """
        try:
            self.connect()
            self.login()
            self.select_folder(folder_name)

            email_ids = self.search_emails()
            max_emails = max_emails or MAIL_CONFIG["max_emails_per_fetch"]
            
            # 限制处理的邮件数量
            if len(email_ids) > max_emails:
                email_ids = email_ids[-max_emails:]  # 取最新的邮件
            
            email_info_list = []
            for email_id in email_ids:
                email_info = self.parse_email(email_id)
                if email_info:
                    email_info_list.append(email_info)
            
            logger.info(f"成功解析 {len(email_info_list)} 封邮件")
            return email_info_list
        except Exception as e:
            logger.error(f"读取邮件失败: {e}")
            return []
        finally:
            if self.imap_client:
                try:
                    self.imap_client.logout()
                except:
                    pass

def process_ticket_emails(emails, db):
    """
    处理车票相关邮件
    :param emails: 邮件列表
    :param db: 数据库对象
    :return: dict 处理结果统计
    """
    stats = {
        'total_processed': 0,
        'tickets_added': 0,
        'refunds_processed': 0,
        'errors': 0
    }
    
    for email_info in emails:
        try:
            subject = email_info['subject']
            content = email_info['content']
            
            logger.info(f"处理邮件: {subject}")
            
            if subject == "网上购票系统-用户支付通知":
                # 处理购票信息
                ticket_info = parse_ticket_info(content)
                if validate_ticket_info(ticket_info):
                    # 检查乘客姓名过滤
                    if PASSENGER_FILTER and ticket_info.get('passenger_name') != PASSENGER_FILTER:
                        logger.info(f"跳过非目标乘客: {ticket_info.get('passenger_name')}")
                        continue
                    
                    result = db.add_ticket(ticket_info)
                    if result:
                        stats['tickets_added'] += 1
                        logger.info(f"购票: {ticket_info['order_id']} {ticket_info['passenger_name']} {ticket_info['departure_time']} {ticket_info['departure_station']}-{ticket_info['arrival_station']} {ticket_info['train_number']} {ticket_info['carriage_number']} {ticket_info['seat_number']} {ticket_info['seat_type']} {ticket_info['price']}元")
                    else:
                        stats['errors'] += 1
                else:
                    logger.warning(f"车票信息验证失败: {ticket_info}")
                    stats['errors'] += 1

            elif subject == "网上购票系统-候补订单兑现成功通知":
                # 处理候补订单信息
                ticket_info = parse_ticket_info(content)
                if validate_ticket_info(ticket_info):
                    # 检查乘客姓名过滤
                    if PASSENGER_FILTER and ticket_info.get('passenger_name') != PASSENGER_FILTER:
                        logger.info(f"跳过非目标乘客: {ticket_info.get('passenger_name')}")
                        continue
                    
                    ticket_info['is_waiting'] = True
                    result = db.add_ticket(ticket_info)
                    if result:
                        stats['tickets_added'] += 1
                        logger.info(f"候补: {ticket_info['order_id']} {ticket_info['passenger_name']} {ticket_info['departure_time']} {ticket_info['departure_station']}-{ticket_info['arrival_station']} {ticket_info['train_number']} {ticket_info['carriage_number']} {ticket_info['seat_number']} {ticket_info['seat_type']} {ticket_info['price']}元")
                    else:
                        stats['errors'] += 1
                else:
                    logger.warning(f"候补车票信息验证失败: {ticket_info}")
                    stats['errors'] += 1

            elif subject == "网上购票系统-用户退票通知":
                # 处理退票信息
                refund_info = parse_refund_info(content)
                if refund_info.get('order_id'):
                    result = db.refund_ticket(
                        order_id=refund_info['order_id'],
                        service_fee=refund_info['service_fee']
                    )
                    if result:
                        stats['refunds_processed'] += 1
                        logger.info(f"退票: {refund_info['order_id']} 票价:{refund_info['price']}元 应退:{refund_info['refund_amount']}元 手续费:{refund_info['service_fee']}元")
                    else:
                        stats['errors'] += 1
                else:
                    logger.warning(f"退票信息解析失败: {refund_info}")
                    stats['errors'] += 1
            
            stats['total_processed'] += 1
            
        except Exception as e:
            logger.error(f"处理邮件失败: {e}")
            stats['errors'] += 1
    
    return stats

def main():
    """
    主函数：读取邮件并处理车票信息
    """
    try:
        logger.info("开始处理车票邮件...")
        
        # 创建数据库连接
        db = TicketDB()
        
        # 创建邮件读取器并读取邮件
        mail_reader = MailReader()
        emails = mail_reader.read_emails()
        
        if not emails:
            logger.info("没有找到邮件")
            return
        
        # 处理车票邮件
        stats = process_ticket_emails(emails, db)
        
        # 输出统计信息
        logger.info(f"处理完成 - 总计: {stats['total_processed']}, 新增车票: {stats['tickets_added']}, 退票处理: {stats['refunds_processed']}, 错误: {stats['errors']}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise

if __name__ == "__main__":
    main() 