# -*- coding: utf-8 -*-
"""
12306 车票信息管理系统配置示例
请复制此文件为 config.py 并根据您的实际情况修改配置
"""

# 邮箱配置示例
EMAIL_CONFIG = {
    # 163邮箱配置
    "imap_host": "imap.163.com",
    "email_user": "your-email@163.com",
    "email_pwd": "your-password",  # 使用邮箱授权码，不是登录密码
    "folder_name": "12306"
}

# 其他邮箱配置示例
EMAIL_CONFIG_QQ = {
    # QQ邮箱配置
    "imap_host": "imap.qq.com",
    "email_user": "your-email@qq.com",
    "email_pwd": "your-authorization-code",  # QQ邮箱授权码
    "folder_name": "12306"
}

EMAIL_CONFIG_GMAIL = {
    # Gmail配置
    "imap_host": "imap.gmail.com",
    "email_user": "your-email@gmail.com",
    "email_pwd": "your-app-password",  # Gmail应用专用密码
    "folder_name": "12306"
}

EMAIL_CONFIG_OUTLOOK = {
    # Outlook配置
    "imap_host": "outlook.office365.com",
    "email_user": "your-email@outlook.com",
    "email_pwd": "your-password",
    "folder_name": "12306"
}

# 乘客姓名过滤（可选）
PASSENGER_FILTER = "温阳光"  # 只处理指定乘客的车票信息，设为None则不过滤

# 数据库配置
DATABASE_CONFIG = {
    "db_path": "ticket/tickets.db"  # 数据库文件路径
}

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",  # 监听所有网络接口
    "port": 8888,       # 服务端口
    "debug": False      # 调试模式
}

# 邮件处理配置
MAIL_CONFIG = {
    "auto_refresh_interval": 3600,  # 自动刷新间隔（秒），1小时
    "max_emails_per_fetch": 100,    # 每次最多处理的邮件数量
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",  # 日志级别: DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "ticket_manager.log"
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