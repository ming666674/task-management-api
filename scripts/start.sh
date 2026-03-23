#!/bin/bash

cd "$(dirname "$0")/.."

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 安装依赖
pip install -r requirements.txt

# 启动服务
nohup python run.py > app.log 2>&1 &
echo "Service started. PID: $!"
echo $! > app.pid