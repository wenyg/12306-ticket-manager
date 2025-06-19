# -*- coding: utf-8 -*-
"""
12306 车票信息管理系统配置文件
"""

# 邮箱配置
EMAIL_CONFIG = {
    "imap_host": "imap.163.com",  # 邮箱服务器地址
    "email_user": "your-email@163.com",  # 邮箱账号
    "email_pwd": "your-password",  # 邮箱密码或授权码
    "folder_name": "12306"  # 存放12306邮件的文件夹
}

# 乘客姓名过滤（可选）
PASSENGER_FILTER = "温阳光"  # 只处理指定乘客的车票信息，设为None则不过滤

# 数据库配置
DATABASE_CONFIG = {
    "db_path": "ticket/tickets.db"  # 数据库文件路径
}

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8888,
    "debug": False
}

# 邮件处理配置
MAIL_CONFIG = {
    "auto_refresh_interval": 3600,  # 自动刷新间隔（秒）
    "max_emails_per_fetch": 100,  # 每次最多处理的邮件数量
}

# 支持的邮箱服务商配置
EMAIL_PROVIDERS = {
    "163": {
        "imap_host": "imap.163.com",
        "smtp_host": "smtp.163.com",
        "port": 993
    },
    "qq": {
        "imap_host": "imap.qq.com",
        "smtp_host": "smtp.qq.com",
        "port": 993
    },
    "gmail": {
        "imap_host": "imap.gmail.com",
        "smtp_host": "smtp.gmail.com",
        "port": 993
    },
    "outlook": {
        "imap_host": "outlook.office365.com",
        "smtp_host": "smtp.office365.com",
        "port": 993
    }
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "ticket_manager.log"
} 