# 更新日誌

## Feature: Gait Integration (feature/gait-integration)

### 新增功能

1. **支援處理過的影片顯示**
   - Gait 系統處理後的影片會顯示在網頁上
   - 新增 `/api/video/{filename}` endpoint 提供影片檔案

2. **支援多個識別結果**
   - 一次可以識別多個人
   - 結果以卡片網格形式顯示

3. **整合 identity_map.json**
   - 自動載入 `gait/identity_map.json`
   - 根據識別結果自動映射到個人資訊

### 修改的檔案

#### 後端
- `backend/app/models/schemas.py` - 新增 `RecognitionResponse` 模型
- `backend/app/services/gait_service.py` - 更新為支援處理過的影片和多個結果
- `backend/app/api/routes.py` - 更新 API 端點，新增影片下載功能

#### 前端
- `frontend/src/types/index.ts` - 更新類型定義
- `frontend/src/services/api.ts` - 更新 API 服務
- `frontend/src/components/ResultDisplay.tsx` - 支援顯示處理過的影片和多個結果
- `frontend/src/components/PersonCard.tsx` - 更新個人資訊顯示
- `frontend/src/App.tsx` - 更新主應用程式

#### Gait 系統
- `gait/process.py` - 新的橋接層，支援處理過的影片和 identity_map 映射
- `gait/main.py` - 範例實作，展示如何處理影片和回傳識別結果

### API 變更

#### POST /api/upload
**舊格式：**
```json
{
  "probe_id": "probe_001",
  "gallery_id": "gallery_001",
  "person_info": { ... }
}
```

**新格式：**
```json
{
  "probe_id": "probe_001",
  "processed_video_url": "/api/video/probe_001_processed.mp4",
  "recognition_results": [
    {
      "gallery_id": "gallery_1",
      "person_id": "001",
      "name": "Sam Wu",
      "Department": "Electrical Engineering",
      ...
    }
  ],
  "total_detected": 2
}
```

#### 新增 GET /api/video/{filename}
提供處理過的影片檔案下載

### 使用說明

1. **Gait main.py 函數簽名**
```python
def main(video_path: str) -> Tuple[str, Dict]:
    """
    處理影片並進行步態識別
    
    Returns:
        tuple: (processed_video_path, recognition_dict)
            - processed_video_path: 處理過的影片檔案路徑
            - recognition_dict: 識別結果字典，格式為 {gallery_id: person_id}
    """
    # 您的處理邏輯
    return processed_video_path, recognition_dict
```

2. **identity_map.json 格式**
```json
{
  "gallery_1": {
    "001": {
      "name": "Sam Wu",
      "Department": "Electrical Engineering",
      "Year in school": "Junior",
      "photo_url": "https://example.com/photos/sam_wu.jpg"
    }
  }
}
```

3. **識別結果字典格式**
```python
{
  "gallery_1": "001",  # gallery_id: person_id
  "gallery_2": "002"
}
```

### 注意事項

- 處理過的影片會儲存在 `backend/data/processed/` 目錄
- 確保 `gait/identity_map.json` 存在且格式正確
- 支援多個識別結果，結果會自動映射到個人資訊

