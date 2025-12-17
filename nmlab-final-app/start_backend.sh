#!/bin/bash
# 啟動後端服務

# 取得腳本所在目錄
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/backend" || exit 1

# 檢查並終止占用端口 8000 的進程
PORT=8000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "發現端口 $PORT 已被占用，正在終止舊進程..."
    lsof -ti :$PORT | xargs kill -9 2>/dev/null
    sleep 1
    echo "已清理端口 $PORT"
fi

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "建立虛擬環境..."
    python3 -m venv venv
fi

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
echo "安裝依賴..."
pip install -q -r requirements.txt

# 啟動服務
echo "啟動後端服務..."
echo "後端將在 http://localhost:$PORT 運行"
echo "API 文件: http://localhost:$PORT/docs"
echo ""
uvicorn app.main:app --reload --port $PORT --host 0.0.0.0

