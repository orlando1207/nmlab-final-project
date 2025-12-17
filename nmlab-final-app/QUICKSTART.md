# 快速開始指南

## 前置需求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 啟動步驟

### 方法一：使用啟動腳本（推薦）

開啟兩個終端視窗：

**終端 1 - 啟動後端：**
```bash
./start_backend.sh
```

**終端 2 - 啟動前端：**
```bash
./start_frontend.sh
```

### 方法二：手動啟動

**1. 啟動後端**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

後端將在 http://localhost:8000 運行
API 文件：http://localhost:8000/docs

**2. 啟動前端**

```bash
cd frontend
npm install
npm run dev
```

前端將在 http://localhost:5173 運行

## 測試流程

1. 開啟瀏覽器訪問 http://localhost:5173
2. 準備一個 .mp4 影片檔案（任何 .mp4 檔案都可以，Mock 系統會隨機回傳結果）
3. 點擊上傳區域或拖曳影片檔案
4. 點擊「上傳並識別」按鈕
5. 等待處理完成（約 0.5 秒）
6. 查看識別結果與個人資訊

## Mock Gait 系統說明

目前的 Mock 系統 (`gait/process.py`) 會：
- 接收任何 .mp4 檔案
- 隨機選擇一個 gallery ID (gallery_001, gallery_002, 或 gallery_003)
- 回傳 `{probe_id: gallery_id}` 格式的結果

## 整合真實 Gait 系統

當您準備好整合真實的 Gait 系統時：

1. 將您的 Gait 專案檔案放入 `gait/` 目錄
2. 修改 `gait/process.py` 中的 `process_video` 函數
3. 確保函數簽名保持一致：
   ```python
   def process_video(video_path: str, probe_id: str) -> Dict[str, str]:
       # 您的 Gait 識別邏輯
       return {probe_id: gallery_id}
   ```

## 個人資訊設定

編輯 `backend/data/person_info.json` 來新增或修改個人資訊：

```json
{
  "gallery_001": {
    "id": "gallery_001",
    "name": "姓名",
    "photo": "/photos/person_001.jpg",
    "department": "系所",
    "student_id": "學號",
    "email": "email@example.com"
  }
}
```

## 疑難排解

### 後端無法啟動
- 確認 Python 版本 >= 3.8
- 確認已安裝所有依賴：`pip install -r requirements.txt`
- 檢查端口 8000 是否被占用

### 前端無法啟動
- 確認 Node.js 版本 >= 16
- 刪除 `node_modules` 並重新安裝：`rm -rf node_modules && npm install`
- 檢查端口 5173 是否被占用

### 上傳失敗
- 確認後端服務正在運行
- 檢查瀏覽器控制台的錯誤訊息
- 確認檔案格式為 .mp4
- 確認檔案大小 < 100MB

### CORS 錯誤
- 確認後端的 CORS 設定包含前端 URL
- 檢查 `backend/app/main.py` 中的 `allow_origins`

