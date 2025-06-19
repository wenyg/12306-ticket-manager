# -*- coding: utf-8 -*-
import re
import json
from collections import Counter
from datetime import datetime

def parse_ticket_info(text):
    """
    解析车票信息
    :param text: 邮件内容文本
    :return: dict 解析后的车票信息
    """
    # 定义正则表达式模式
    patterns = {
        'order_id': r'订单号码([A-Z0-9]+)',
        'passenger_name': r'车票信息如下:\d+\.([^,]+)',
        'departure_time': r'(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})开',
        'route': r'开,([^-]+)-([^,]+),',
        'train_number': r'([A-Z0-9]+次列车)',
        'carriage_number': r'(\d+车)',
        'seat_number': r'(\d+[A-Z]号|\d+号|无座)',
        'seat_type': r'(无座|硬座|硬卧|软卧|二等座|一等座|二等卧)',
        'price': r'票价(\d+\.?\d*)元',
    }
    
    # 解析结果
    result = {}
    
    # 提取订单号
    order_match = re.search(patterns['order_id'], text)
    if order_match:
        result['order_id'] = order_match.group(1)
    
    # 提取姓名
    name_match = re.search(patterns['passenger_name'], text)
    if name_match:
        result['passenger_name'] = name_match.group(1)
    
    # 提取乘车时间
    time_match = re.search(patterns['departure_time'], text)
    if time_match:
        time_str = time_match.group(1)
        # 将中文日期格式转换为datetime对象
        result['departure_time'] = datetime.strptime(time_str, '%Y年%m月%d日%H:%M')
    
    # 提取路线
    route_match = re.search(patterns['route'], text)
    if route_match:
        result['departure_station'] = route_match.group(1)
        result['arrival_station'] = route_match.group(2)
    
    # 提取车次
    train_match = re.search(patterns['train_number'], text)
    if train_match:
        result['train_number'] = train_match.group(1)
    
    # 提取车厢号
    carriage_match = re.search(patterns['carriage_number'], text)
    if carriage_match:
        result['carriage_number'] = carriage_match.group(1)
    
    # 提取座位号
    seat_match = re.search(patterns['seat_number'], text)
    if seat_match:
        result['seat_number'] = seat_match.group(1)
    else:
        result['seat_number'] = ''
    
    # 提取座位类型
    seat_type_match = re.search(patterns['seat_type'], text)
    if seat_type_match:
        result['seat_type'] = seat_type_match.group(1)
    else:
        result['seat_type'] = ''
    
    # 提取票价
    price_match = re.search(patterns['price'], text)
    if price_match:
        result['price'] = float(price_match.group(1))
    else:
        result['price'] = 0.0
    
    return result

def parse_refund_info(text):
    """
    解析退票信息
    :param text: 邮件内容文本
    :return: dict 解析后的退票信息
    """
    # 定义正则表达式模式
    patterns = {
        'order_id': r'订单号码([A-Z0-9]+)',
        'price': r'票价(\d+\.?\d*)元',
        'refund_amount': r'应退票款(\d+\.?\d*)元'
    }
    
    # 解析结果
    result = {}
    
    # 提取订单号
    order_match = re.search(patterns['order_id'], text)
    if order_match:
        result['order_id'] = order_match.group(1)
    
    # 提取票价
    price_match = re.search(patterns['price'], text)
    if price_match:
        result['price'] = float(price_match.group(1))
    else:
        result['price'] = 0.0
    
    # 提取应退票款
    refund_match = re.search(patterns['refund_amount'], text)
    if refund_match:
        result['refund_amount'] = float(refund_match.group(1))
    else:
        result['refund_amount'] = 0.0
    
    # 计算手续费（票价减去应退票款）
    result['service_fee'] = result['price'] - result['refund_amount']
    
    return result

def validate_ticket_info(ticket_info):
    """
    验证车票信息的完整性
    :param ticket_info: 车票信息字典
    :return: bool 是否有效
    """
    required_fields = [
        'order_id', 'passenger_name', 'departure_time', 
        'departure_station', 'arrival_station', 'train_number',
        'carriage_number', 'seat_type', 'price'
    ]
    
    for field in required_fields:
        if field not in ticket_info or not ticket_info[field]:
            return False
    
    return True

def clean_text_content(text):
    """
    清理文本内容，去除多余字符
    :param text: 原始文本
    :return: str 清理后的文本
    """
    # 删除不需要的部分
    unwanted_keywords = [
        "温馨提示", 
        "为了确保", 
        "按购票时所使用在线支付工具的有关规定"
    ]
    
    for keyword in unwanted_keywords:
        if keyword in text:
            text = text.split(keyword)[0]
    
    # 截取从"订单号码"开始的部分
    if "订单号码" in text:
        text = "订单号码" + text.split("订单号码")[1]

    # 替换中文标点为英文标点，并去除空格
    replace_map = {
        "，": ",",
        "：": ":",
        "。": ".",
        "―": "-",
    }
    for old, new in replace_map.items():
        text = text.replace(old, new)
    
    # 去除所有空格
    text = text.replace(" ", "")

    # 保留"温阳光"之前和之后到"票价"部分的内容
    match = re.search(r"(.*温阳光.*?票价[\d\.]+元)", text)
    if match:
        text = match.group(0)

    return text 