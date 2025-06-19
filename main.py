# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from ticket.models import TicketDB
from tools.mail import main as mail_main
from config import SERVER_CONFIG, LOGGING_CONFIG
import os

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="12306 车票信息管理系统",
    description="基于邮箱爬取12306车票信息并进行可视化展示的系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    根路径，重定向到车票页面
    """
    return {"message": "12306 车票信息管理系统", "docs": "/docs", "tickets": "/tickets"}

@app.get("/tickets")
async def get_all_tickets():
    """
    获取所有车票信息
    """
    try:
        db = TicketDB()
        tickets = db.get_all_tickets()
        db.close()
        
        logger.info(f"成功获取 {len(tickets)} 张车票信息")
        
        return {
            "total": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        logger.error(f"获取车票信息失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取车票信息失败: {str(e)}"
        )

@app.get("/tickets/stats")
async def get_ticket_statistics():
    """
    获取车票统计信息
    """
    try:
        db = TicketDB()
        stats = db.get_statistics()
        db.close()
        
        logger.info("成功获取车票统计信息")
        
        return stats
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取统计信息失败: {str(e)}"
        )

@app.get("/tickets/range")
async def get_tickets_by_date_range(start_date: str, end_date: str):
    """
    根据日期范围获取车票信息
    :param start_date: 开始日期 (YYYY-MM-DD)
    :param end_date: 结束日期 (YYYY-MM-DD)
    """
    try:
        db = TicketDB()
        tickets = db.get_tickets_by_date_range(start_date, end_date)
        db.close()
        
        logger.info(f"成功获取 {start_date} 到 {end_date} 的车票信息，共 {len(tickets)} 张")
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        logger.error(f"获取日期范围车票信息失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取日期范围车票信息失败: {str(e)}"
        )

@app.get("/update_ticket")
async def update_ticket():
    """
    手动更新车票信息（从邮箱读取）
    """
    try:
        logger.info("开始手动更新车票信息")
        mail_main()
        logger.info("车票信息更新完成")
        
        return {
            "message": "Ticket updated successfully",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"更新车票信息失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"更新车票信息失败: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    try:
        db = TicketDB()
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"健康检查失败: {str(e)}"
        )

@app.get("/tickets/web", response_class=HTMLResponse)
async def get_tickets_web():
    """
    返回车票信息的Web页面
    """
    try:
        # 读取HTML文件
        html_file_path = "static/index.html"
        if os.path.exists(html_file_path):
            with open(html_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        else:
            # 如果HTML文件不存在，返回简单的HTML页面
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>12306 车票信息管理系统</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .api-link { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
                    .api-link a { color: #007bff; text-decoration: none; }
                    .api-link a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚄 12306 车票信息管理系统</h1>
                        <p>基于邮箱爬取12306车票信息并进行可视化展示的系统</p>
                    </div>
                    
                    <h2>📊 API 接口</h2>
                    <div class="api-link">
                        <a href="/tickets">📋 获取所有车票信息</a>
                    </div>
                    <div class="api-link">
                        <a href="/tickets/stats">📈 获取统计信息</a>
                    </div>
                    <div class="api-link">
                        <a href="/update_ticket">🔄 手动更新车票信息</a>
                    </div>
                    <div class="api-link">
                        <a href="/health">💚 健康检查</a>
                    </div>
                    <div class="api-link">
                        <a href="/docs">📖 API 文档</a>
                    </div>
                    
                    <h2>🚀 快速开始</h2>
                    <p>1. 配置 <code>config.py</code> 文件中的邮箱信息</p>
                    <p>2. 运行 <code>python main.py</code> 启动服务</p>
                    <p>3. 访问 <a href="/tickets">车票信息页面</a></p>
                    
                    <h2>📝 使用说明</h2>
                    <p>系统会自动从配置的邮箱中读取12306的购票、退票、候补通知邮件，并解析车票信息。</p>
                    <p>支持的车票状态：正常、候补、退票</p>
                    <p>支持的功能：日历视图、统计分析、移动端适配</p>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"返回Web页面失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"返回Web页面失败: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    logger.info("启动12306车票信息管理系统...")
    logger.info(f"服务器配置: {SERVER_CONFIG}")
    
    uvicorn.run(
        app, 
        host=SERVER_CONFIG["host"], 
        port=SERVER_CONFIG["port"],
        log_level="info"
    ) 