# 影片儲存說明

## 儲存位置與方式

### 1. 上傳的原始影片

**位置：** `backend/data/uploads/`

**儲存流程：**
1. 使用者上傳影片 → 儲存到 `backend/data/uploads/{probe_id}.mp4`
2. 傳送給 Gait 系統處理
3. **處理完成後自動刪除**（節省空間）

**程式碼位置：** `backend/app/api/routes.py` 第 119 行
```python
# 清理上傳的原始檔案
if saved_path.exists():
    saved_path.unlink()
```

### 2. 處理過的影片

**位置：** `backend/data/processed/`

**儲存流程：**
1. Gait 系統處理後產生處理過的影片
2. 移動到 `backend/data/processed/{probe_id}_processed.mp4`
3. **保留供網頁顯示和下載**

**程式碼位置：** `backend/app/api/routes.py` 第 91-99 行
```python
# 將處理過的影片移動到 processed 目錄
processed_path = Path(processed_video_path)
if processed_path.exists():
    if processed_path.parent != PROCESSED_DIR:
        processed_filename = f"{probe_id}_processed{processed_path.suffix}"
        target_path = PROCESSED_DIR / processed_filename
        shutil.move(str(processed_path), str(target_path))
```

### 3. 影片存取

**API Endpoint：** `GET /api/video/{filename}`

**範例：**
- URL: `http://localhost:8000/api/video/probe_abc123_processed.mp4`
- 檔案位置: `backend/data/processed/probe_abc123_processed.mp4`

## 檔案清理建議

### 自動清理（可選）

如果需要定期清理舊的處理過的影片，可以：

1. **設定保留時間**：例如只保留 7 天內的影片
2. **設定最大數量**：例如最多保留 100 個影片
3. **手動清理**：定期刪除 `backend/data/processed/` 中的舊檔案

### 手動清理腳本範例

```python
# scripts/cleanup_processed_videos.py
from pathlib import Path
import time
from datetime import datetime, timedelta

PROCESSED_DIR = Path("backend/data/processed")
RETENTION_DAYS = 7  # 保留 7 天

def cleanup_old_videos():
    cutoff_time = time.time() - (RETENTION_DAYS * 24 * 60 * 60)
    
    for video_file in PROCESSED_DIR.glob("*.mp4"):
        if video_file.stat().st_mtime < cutoff_time:
            video_file.unlink()
            print(f"已刪除舊影片: {video_file.name}")

if __name__ == "__main__":
    cleanup_old_videos()
```

## 目錄結構

```
backend/data/
├── uploads/          # 上傳的原始影片（處理後自動刪除）
│   └── .gitkeep
└── processed/       # 處理過的影片（保留供顯示）
    └── .gitkeep
```

## 注意事項

1. **空間管理**：處理過的影片會持續累積，建議定期清理
2. **檔案命名**：使用 `{probe_id}_processed.mp4` 格式，避免衝突
3. **權限設定**：確保目錄有寫入權限
4. **備份考量**：如果需要保留處理過的影片，考慮備份策略

