#!/bin/bash
# 停止後端服務

PORT=8000

if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "正在停止端口 $PORT 上的後端服務..."
    PIDS=$(lsof -ti :$PORT)
    if [ -n "$PIDS" ]; then
        echo "$PIDS" | xargs kill -9 2>/dev/null
        echo "已停止後端服務"
    else
        echo "未找到運行中的後端服務"
    fi
else
    echo "端口 $PORT 上沒有運行中的服務"
fi


