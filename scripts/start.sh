#!/bin/bash

# 12306 车票信息管理系统启动脚本

echo "🚄 启动12306车票信息管理系统..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查配置文件是否存在
if [ ! -f "config.py" ]; then
    echo "❌ 错误: 未找到config.py配置文件"
    echo "请先运行 python scripts/setup.py 进行安装配置"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "⚠️  警告: 依赖包未安装，正在安装..."
    pip3 install -r requirements.txt
fi

# 启动服务
echo "✅ 启动服务..."
python3 main.py 