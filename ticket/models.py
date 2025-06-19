# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime
from config import DATABASE_CONFIG

class TicketDB:
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = DATABASE_CONFIG["db_path"]
        
        # 确保数据库目录存在
        db_dir = os.path.dirname(db_name)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            order_id TEXT PRIMARY KEY,
            passenger_name TEXT NOT NULL,
            departure_time DATETIME NOT NULL,
            departure_station TEXT NOT NULL,
            arrival_station TEXT NOT NULL,
            train_number TEXT NOT NULL,
            carriage_number TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            seat_type TEXT NOT NULL,
            price REAL NOT NULL,
            is_waiting BOOLEAN NOT NULL,
            is_refunded BOOLEAN NOT NULL DEFAULT 0,
            is_changed BOOLEAN NOT NULL DEFAULT 0,
            service_fee REAL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()
    
    def add_ticket(self, ticket_info):
        """
        添加或更新票务记录
        :param ticket_info: 包含票务信息的字典
        :return: bool 是否操作成功
        """
        try:
            # 检查是否存在该订单
            self.cursor.execute('SELECT order_id FROM tickets WHERE order_id = ?', (ticket_info['order_id'],))
            exists = self.cursor.fetchone() is not None

            if exists:
                # 更新现有记录
                self.cursor.execute('''
                UPDATE tickets SET
                    passenger_name = ?,
                    departure_time = ?,
                    departure_station = ?,
                    arrival_station = ?,
                    train_number = ?,
                    carriage_number = ?,
                    seat_number = ?,
                    seat_type = ?,
                    price = ?,
                    is_waiting = ?,
                    is_refunded = ?,
                    is_changed = ?,
                    service_fee = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
                ''', (
                    ticket_info['passenger_name'],
                    ticket_info['departure_time'],
                    ticket_info['departure_station'],
                    ticket_info['arrival_station'],
                    ticket_info['train_number'],
                    ticket_info['carriage_number'],
                    ticket_info['seat_number'],
                    ticket_info['seat_type'],
                    ticket_info['price'],
                    ticket_info.get('is_waiting', False),
                    ticket_info.get('is_refunded', False),
                    ticket_info.get('is_changed', False),
                    ticket_info.get('service_fee', 0.0),
                    ticket_info['order_id']
                ))
            else:
                # 插入新记录
                self.cursor.execute('''
                INSERT INTO tickets (
                    order_id, passenger_name, departure_time, departure_station,
                    arrival_station, train_number, carriage_number, seat_number,
                    seat_type, price, is_waiting, is_refunded, is_changed, service_fee
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ticket_info['order_id'],
                    ticket_info['passenger_name'],
                    ticket_info['departure_time'],
                    ticket_info['departure_station'],
                    ticket_info['arrival_station'],
                    ticket_info['train_number'],
                    ticket_info['carriage_number'],
                    ticket_info['seat_number'],
                    ticket_info['seat_type'],
                    ticket_info['price'],
                    ticket_info.get('is_waiting', False),
                    ticket_info.get('is_refunded', False),
                    ticket_info.get('is_changed', False),
                    ticket_info.get('service_fee', 0.0)
                ))
                print(f"添加新订单 {ticket_info['order_id']} 的信息")
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"操作票务记录失败: {e}")
            return False

    def refund_ticket(self, order_id, service_fee):
        """
        更新退票信息
        :param order_id: 订单号
        :param service_fee: 手续费
        :return: bool 是否退票成功
        """
        try:
            self.cursor.execute('''
            UPDATE tickets 
            SET is_refunded = 1, service_fee = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
            ''', (service_fee, order_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新退票信息失败: {e}")
            return False

    def get_all_tickets(self):
        """
        获取所有车票信息
        :return: list 车票信息列表
        """
        try:
            self.cursor.execute('''
            SELECT * FROM tickets 
            ORDER BY departure_time DESC
            ''')
            
            tickets = self.cursor.fetchall()
            
            if not tickets:
                return []
            
            result = []
            for row in tickets:
                ticket = {
                    'order_id': row[0],
                    'passenger_name': row[1],
                    'departure_time': row[2],
                    'departure_station': row[3],
                    'arrival_station': row[4],
                    'train_number': row[5],
                    'carriage_number': row[6],
                    'seat_number': row[7],
                    'seat_type': row[8],
                    'price': row[9],
                    'is_waiting': bool(row[10]),
                    'is_refunded': bool(row[11]),
                    'is_changed': bool(row[12]),
                    'service_fee': row[13],
                    'created_at': row[14],
                    'updated_at': row[15]
                }
                result.append(ticket)
            
            return result
                
        except sqlite3.Error as e:
            print(f"获取车票信息失败: {e}")
            return []

    def get_tickets_by_date_range(self, start_date, end_date):
        """
        根据日期范围获取车票信息
        :param start_date: 开始日期 (YYYY-MM-DD)
        :param end_date: 结束日期 (YYYY-MM-DD)
        :return: list 车票信息列表
        """
        try:
            self.cursor.execute('''
            SELECT * FROM tickets 
            WHERE DATE(departure_time) BETWEEN ? AND ?
            ORDER BY departure_time DESC
            ''', (start_date, end_date))
            
            tickets = self.cursor.fetchall()
            
            if not tickets:
                return []
            
            result = []
            for row in tickets:
                ticket = {
                    'order_id': row[0],
                    'passenger_name': row[1],
                    'departure_time': row[2],
                    'departure_station': row[3],
                    'arrival_station': row[4],
                    'train_number': row[5],
                    'carriage_number': row[6],
                    'seat_number': row[7],
                    'seat_type': row[8],
                    'price': row[9],
                    'is_waiting': bool(row[10]),
                    'is_refunded': bool(row[11]),
                    'is_changed': bool(row[12]),
                    'service_fee': row[13],
                    'created_at': row[14],
                    'updated_at': row[15]
                }
                result.append(ticket)
            
            return result
                
        except sqlite3.Error as e:
            print(f"获取车票信息失败: {e}")
            return []

    def get_statistics(self):
        """
        获取统计信息
        :return: dict 统计信息
        """
        try:
            # 总车票数（不包括退票）
            self.cursor.execute('''
            SELECT COUNT(*) FROM tickets WHERE is_refunded = 0
            ''')
            total_tickets = self.cursor.fetchone()[0]
            
            # 候补车票数
            self.cursor.execute('''
            SELECT COUNT(*) FROM tickets WHERE is_waiting = 1 AND is_refunded = 0
            ''')
            waiting_tickets = self.cursor.fetchone()[0]
            
            # 总金额（不包括退票）
            self.cursor.execute('''
            SELECT SUM(price) FROM tickets WHERE is_refunded = 0
            ''')
            total_amount = self.cursor.fetchone()[0] or 0
            
            # 退票次数
            self.cursor.execute('''
            SELECT COUNT(*) FROM tickets WHERE is_refunded = 1
            ''')
            refund_count = self.cursor.fetchone()[0]
            
            # 总手续费
            self.cursor.execute('''
            SELECT SUM(service_fee) FROM tickets
            ''')
            total_fees = self.cursor.fetchone()[0] or 0
            
            return {
                'total_tickets': total_tickets,
                'waiting_tickets': waiting_tickets,
                'total_amount': total_amount,
                'refund_count': refund_count,
                'total_fees': total_fees,
                'avg_price': total_amount / total_tickets if total_tickets > 0 else 0,
                'waiting_percentage': (waiting_tickets / total_tickets * 100) if total_tickets > 0 else 0
            }
                
        except sqlite3.Error as e:
            print(f"获取统计信息失败: {e}")
            return {}

    def print_all_tickets(self):
        """
        打印所有车票信息
        """
        tickets = self.get_all_tickets()
        
        if not tickets:
            print("当前没有车票记录")
            return
        
        print(f"\n共找到 {len(tickets)} 张车票记录：")
        
        for ticket in tickets:
            print(f"\n订单号: {ticket['order_id']}")
            print(f"乘客姓名: {ticket['passenger_name']}")
            print(f"出发时间: {ticket['departure_time']}")
            print(f"出发站: {ticket['departure_station']}")
            print(f"到达站: {ticket['arrival_station']}")
            print(f"车次: {ticket['train_number']}")
            print(f"车厢号: {ticket['carriage_number']}")
            print(f"座位号: {ticket['seat_number']}")
            print(f"座位类型: {ticket['seat_type']}")
            print(f"票价: {ticket['price']}元")
            print(f"候补状态: {'是' if ticket['is_waiting'] else '否'}")
            print(f"退票状态: {'是' if ticket['is_refunded'] else '否'}")
            print(f"改签状态: {'是' if ticket['is_changed'] else '否'}")
            if ticket['service_fee'] > 0:
                print(f"手续费: {ticket['service_fee']}元")
            print("-" * 50)
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = TicketDB()
    db.print_all_tickets()
    db.close() 