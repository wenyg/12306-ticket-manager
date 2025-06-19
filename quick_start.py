#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306 车票信息管理系统快速启动脚本
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
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version}")

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'fastapi', 'uvicorn', 'beautifulsoup4', 
        'chardet', 'requests', 'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  缺少依赖包: {', '.join(missing_packages)}")
        print("正在安装依赖包...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ 依赖包安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖包安装失败: {e}")
            sys.exit(1)
    else:
        print("✅ 依赖包检查通过")

def check_config():
    """检查配置文件"""
    if not os.path.exists("config.py"):
        print("⚠️  未找到配置文件 config.py")
        print("正在创建配置文件模板...")
        
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
        return False
    else:
        print("✅ 配置文件检查通过")
        return True

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

def start_server():
    """启动服务器"""
    print("🚀 启动12306车票信息管理系统...")
    print("📱 访问地址: http://localhost:8888")
    print("📖 API文档: http://localhost:8888/docs")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        from main import app
        import uvicorn
        from config import SERVER_CONFIG
        
        uvicorn.run(
            app, 
            host=SERVER_CONFIG["host"], 
            port=SERVER_CONFIG["port"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("🚄 12306 车票信息管理系统快速启动")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 检查依赖包
    check_dependencies()
    
    # 检查配置文件
    config_ready = check_config()
    
    # 初始化数据库
    initialize_database()
    
    if not config_ready:
        print("\n" + "=" * 50)
        print("⚠️  请先配置邮箱信息:")
        print("1. 编辑 config.py 文件")
        print("2. 配置您的邮箱账号和密码")
        print("3. 重新运行此脚本")
        print("\n📖 更多信息请查看 README.md 文件")
        return
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 