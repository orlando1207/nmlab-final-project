# Gait Recognition Web Application - 專案規劃

## 專案概述

建立一個網頁應用程式，讓使用者上傳影片 (.mp4)，透過 Gait 系統進行步態識別，並顯示識別結果與個人資訊。

## 系統架構

```
使用者上傳影片 (.mp4)
    ↓
前端網頁 (TypeScript/React)
    ↓
後端 API (Python/FastAPI)
    ↓
Gait 識別系統 (Python)
    ↓
結果處理 (dict: Probe → Gallery ID)
    ↓
JSON 映射檔 (ID → 個人資訊)
    ↓
顯示結果到網頁
```

## 技術棧建議

### 前端
- **框架**: React + TypeScript
- **建置工具**: Vite
- **UI 框架**: Tailwind CSS 或 Material-UI
- **HTTP 客戶端**: Axios 或 Fetch API

### 後端
- **框架**: FastAPI (Python)
- **檔案處理**: 處理影片上傳與暫存
- **API**: RESTful API

### 資料格式
- **輸入**: .mp4 影片檔案
- **Gait 輸出**: dict (Probe → Gallery ID)
- **個人資訊**: JSON 檔案 (ID → {姓名, 照片, 其他資料})

## 專案結構

```
nmlab-final-app/
├── frontend/                 # 前端專案
│   ├── src/
│   │   ├── components/       # React 元件
│   │   │   ├── VideoUpload.tsx
│   │   │   ├── ResultDisplay.tsx
│   │   │   └── PersonCard.tsx
│   │   ├── services/        # API 服務
│   │   │   └── api.ts
│   │   ├── types/           # TypeScript 類型定義
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # 後端專案
│   ├── app/
│   │   ├── main.py          # FastAPI 主程式
│   │   ├── api/
│   │   │   └── routes.py    # API 路由
│   │   ├── services/
│   │   │   ├── gait_service.py  # Gait 系統整合
│   │   │   └── person_service.py # 個人資訊處理
│   │   └── models/
│   │       └── schemas.py   # Pydantic 模型
│   ├── data/
│   │   ├── person_info.json # 個人資訊映射檔
│   │   └── uploads/         # 上傳影片暫存目錄
│   ├── requirements.txt
│   └── .env
│
├── gait/                     # Gait 識別系統 (現有專案)
│   └── ...                   # 您的 Gait 專案檔案
│
└── README.md
```

## 實作步驟

### Phase 1: 後端基礎架構
1. 設定 FastAPI 專案
2. 建立檔案上傳 API endpoint
3. 建立 Gait 系統整合介面
4. 實作個人資訊 JSON 讀取功能
5. 建立結果回傳 API endpoint

### Phase 2: 前端基礎架構
1. 設定 React + TypeScript + Vite 專案
2. 建立影片上傳元件
3. 建立 API 服務層
4. 建立結果顯示元件
5. 整合前後端

### Phase 3: 功能完善
1. 錯誤處理與驗證
2. 載入狀態顯示
3. 個人資訊卡片設計
4. 照片顯示功能
5. 響應式設計

### Phase 4: 優化與測試
1. 效能優化
2. 錯誤處理完善
3. 使用者體驗優化
4. 測試與除錯

## API 設計

### POST /api/upload
- **功能**: 上傳影片檔案
- **輸入**: multipart/form-data (video file)
- **輸出**: 
  ```json
  {
    "probe_id": "probe_001",
    "gallery_id": "gallery_123",
    "person_info": {
      "id": "gallery_123",
      "name": "張三",
      "photo": "path/to/photo.jpg",
      "other_info": "..."
    }
  }
  ```

### GET /api/person/{person_id}
- **功能**: 取得個人資訊
- **輸出**: 個人資訊 JSON

## 資料格式範例

### person_info.json
```json
{
  "gallery_123": {
    "id": "gallery_123",
    "name": "張三",
    "photo": "photos/person_123.jpg",
    "department": "資訊工程系",
    "student_id": "B12345678"
  },
  "gallery_456": {
    "id": "gallery_456",
    "name": "李四",
    "photo": "photos/person_456.jpg",
    "department": "電機工程系",
    "student_id": "B87654321"
  }
}
```

### Gait 系統輸出格式 (預期)
```python
{
  "probe_001": "gallery_123",
  "probe_002": "gallery_456"
}
```

## 注意事項

1. **檔案大小限制**: 需要設定合理的影片檔案大小限制
2. **處理時間**: Gait 處理可能需要時間，考慮使用非同步處理或 WebSocket
3. **檔案清理**: 上傳的影片檔案需要定期清理
4. **安全性**: 
   - 檔案類型驗證
   - 檔案大小限制
   - CORS 設定
5. **錯誤處理**: 
   - 影片格式錯誤
   - Gait 處理失敗
   - 找不到對應的個人資訊

## 下一步行動

1. 確認 Gait 系統的具體介面與輸出格式
2. 確認個人資訊 JSON 的完整結構
3. 開始實作後端 API
4. 接著實作前端介面