#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306 车票信息管理系统安装脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version}")

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        sys.exit(1)

def create_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    directories = [
        "ticket",
        "tools", 
        "static",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def create_config_template():
    """创建配置文件模板"""
    print("⚙️ 创建配置文件模板...")
    
    config_template = '''# -*- coding: utf-8 -*-
"""
12306 车票信息管理系统配置文件
请根据您的实际情况修改以下配置
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

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "ticket_manager.log"
}
'''
    
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(config_template)
    
    print("✅ 配置文件模板创建完成: config.py")
    print("⚠️  请编辑 config.py 文件，配置您的邮箱信息")

def initialize_database():
    """初始化数据库"""
    print("🗄️ 初始化数据库...")
    try:
        from ticket.models import TicketDB
        db = TicketDB()
        db.close()
        print("✅ 数据库初始化完成")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("🚄 12306 车票信息管理系统安装程序")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    install_dependencies()
    
    # 创建配置文件模板
    create_config_template()
    
    # 初始化数据库
    initialize_database()
    
    print("\n" + "=" * 50)
    print("🎉 安装完成！")
    print("\n📝 下一步操作:")
    print("1. 编辑 config.py 文件，配置您的邮箱信息")
    print("2. 运行 python main.py 启动服务")
    print("3. 访问 http://localhost:8888 查看车票信息")
    print("\n📖 更多信息请查看 README.md 文件")

if __name__ == "__main__":
    main() 