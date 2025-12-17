#!/bin/bash
# 啟動前端服務

# 取得腳本所在目錄
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/frontend" || exit 1

# 檢查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安裝依賴..."
    npm install
fi

# 啟動開發伺服器
echo "啟動前端服務..."
echo "前端將在 http://localhost:5173 運行"
echo ""
npm run dev

