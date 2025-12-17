# Gait Recognition Web Application

步態識別網頁應用程式 - 支援使用者上傳影片進行步態識別並顯示結果。

## 專案結構

```
nmlab-final-app/
├── backend/          # FastAPI 後端
├── frontend/         # React + TypeScript 前端
├── gait/            # Gait 識別系統 (Mock 測試版本)
└── README.md
```

## 快速開始

### 後端設定

1. 進入後端目錄：
```bash
cd backend
```

2. 建立虛擬環境（建議）：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 啟動後端服務：
```bash
uvicorn app.main:app --reload --port 8000
```

後端 API 文件可在 http://localhost:8000/docs 查看

### 前端設定

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```

3. 啟動開發伺服器：
```bash
npm run dev
```

前端應用程式將在 http://localhost:5173 開啟

## 使用說明

1. 開啟瀏覽器訪問 http://localhost:5173
2. 點擊或拖曳上傳 .mp4 影片檔案
3. 點擊「上傳並識別」按鈕
4. 系統會處理影片並顯示識別結果與個人資訊

## Gait 系統整合

### Mock 模式（預設）

目前使用簡單的 Mock Gait 系統進行測試：
- 位置：`gait/process.py`
- 功能：接收影片檔案，隨機回傳一個 gallery ID
- 輸出格式：`{probe_id: gallery_id}`

### 整合真實 Gait 系統

當您準備好整合真實的 Gait 系統時：

1. 將您的 Gait 專案檔案放入 `gait/` 目錄
2. 確保您的 `gait/main.py` 有一個函數可以：
   - 接收影片路徑（字串）
   - 與 database 進行比較
   - 回傳 gallery_id（字串）
3. 修改 `gait/process.py` 中的導入語句來調用您的函數

詳細整合指南請參考：`gait/INTEGRATION_GUIDE.md`

## 個人資訊映射

個人資訊儲存在 `backend/data/person_info.json`，格式如下：

```json
{
  "gallery_001": {
    "id": "gallery_001",
    "name": "張三",
    "photo": "/photos/person_001.jpg",
    "department": "資訊工程系",
    "student_id": "B12345678",
    "email": "zhang.san@example.com"
  }
}
```

## API 端點

- `POST /api/upload` - 上傳影片並進行識別
- `GET /api/person/{person_id}` - 取得個人資訊
- `GET /api/health` - 健康檢查

## 技術棧

- **後端**: FastAPI (Python)
- **前端**: React + TypeScript + Vite + Tailwind CSS
- **Gait 系統**: Python (Mock 版本)

## 故障排除

如果遇到 `ERR_CONNECTION_REFUSED` 錯誤或其他問題，請參考：
- **故障排除指南**: `TROUBLESHOOTING.md`
- **快速開始**: `QUICKSTART.md`
- **Gait 整合指南**: `gait/INTEGRATION_GUIDE.md`

快速檢查後端服務：
```bash
./check_backend.sh
```

## 注意事項

- 目前僅支援 .mp4 格式的影片檔案
- 檔案大小限制為 100MB
- 上傳的影片會在處理完成後自動刪除
- **重要**: 使用前請確保後端服務已啟動（http://localhost:8000）

