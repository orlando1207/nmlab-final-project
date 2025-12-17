# 故障排除指南

## ERR_CONNECTION_REFUSED 錯誤

這個錯誤表示前端無法連接到後端服務。請按照以下步驟檢查：

### 1. 檢查後端服務是否運行

執行檢查腳本：
```bash
./check_backend.sh
```

或手動檢查：
```bash
curl http://localhost:8000/api/health
```

如果沒有回應，後端服務未運行。

### 2. 啟動後端服務

**方法一：使用啟動腳本**
```bash
./start_backend.sh
```

**方法二：手動啟動**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 確認後端正常運行

打開瀏覽器訪問：
- http://localhost:8000 - 應該看到 API 資訊
- http://localhost:8000/docs - 應該看到 API 文件
- http://localhost:8000/api/health - 應該看到 `{"status":"ok","message":"服務運行中"}`

### 4. 檢查端口衝突

如果端口 8000 被占用，可以：

**選項 A：更改後端端口**
```bash
# 修改啟動命令
uvicorn app.main:app --reload --port 8001
```

然後修改 `frontend/src/services/api.ts`：
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
```

**選項 B：釋放端口 8000**
```bash
# 找出占用端口的進程
lsof -i :8000
# 或
netstat -tulpn | grep 8000

# 終止進程（替換 PID）
kill -9 <PID>
```

### 5. 檢查 CORS 設定

如果後端運行但仍有 CORS 錯誤，檢查 `backend/app/main.py` 中的 CORS 設定：

```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

確保包含您的前端 URL。

### 6. 檢查防火牆設定

確保防火牆允許本地連接：
```bash
# Linux
sudo ufw allow 8000
```

## 其他常見問題

### 前端無法啟動

**問題**: `npm run dev` 失敗

**解決方案**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### 後端導入錯誤

**問題**: `ModuleNotFoundError` 或 `ImportError`

**解決方案**:
1. 確認虛擬環境已啟動
2. 確認所有依賴已安裝：`pip install -r requirements.txt`
3. 檢查 Python 路徑設定

### 影片上傳失敗

**問題**: 上傳時出現錯誤

**解決方案**:
1. 確認檔案格式為 .mp4
2. 確認檔案大小 < 100MB
3. 檢查後端日誌查看詳細錯誤訊息
4. 確認 `backend/data/uploads/` 目錄存在且有寫入權限

### Gait 系統整合問題

**問題**: 無法導入真實的 Gait 系統

**解決方案**:
1. 確認您的 Gait 專案檔案在 `gait/` 目錄中
2. 確認 `gait/main.py` 存在
3. 檢查 `gait/process.py` 中的導入語句
4. 查看 `gait/INTEGRATION_GUIDE.md` 了解詳細整合步驟

## 獲取幫助

如果問題仍然存在：

1. 檢查後端日誌（終端輸出）
2. 檢查瀏覽器控制台（F12）
3. 確認所有服務都在運行
4. 查看相關文件：
   - `README.md` - 基本說明
   - `QUICKSTART.md` - 快速開始
   - `gait/INTEGRATION_GUIDE.md` - Gait 整合指南

