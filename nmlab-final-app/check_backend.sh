#!/bin/bash
# 檢查後端服務是否運行

echo "檢查後端服務狀態..."

# 檢查端口 8000 是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✓ 後端服務正在運行 (端口 8000)"
    
    # 測試健康檢查 endpoint
    if curl -s http://localhost:8000/api/health > /dev/null; then
        echo "✓ 後端 API 回應正常"
        curl -s http://localhost:8000/api/health | python3 -m json.tool
    else
        echo "✗ 後端 API 無法回應"
    fi
else
    echo "✗ 後端服務未運行"
    echo ""
    echo "請執行以下命令啟動後端："
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload --port 8000"
    echo ""
    echo "或使用啟動腳本："
    echo "  ./start_backend.sh"
fi

