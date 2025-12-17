"""
API 路由定義
"""
import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List

from app.models.schemas import RecognitionResponse, PersonInfo, ErrorResponse
from app.services.gait_service import GaitService

router = APIRouter(prefix="/api", tags=["gait"])

# 初始化服務
gait_service = GaitService()

# 上傳目錄 - 使用正式版 Gait 系統的路徑
GAIT_DIR = Path(__file__).parent.parent.parent.parent / "gait"
PROBE_INPUT_DIR = GAIT_DIR / "InputVideos" / "probe"
PROBE_INPUT_DIR.mkdir(parents=True, exist_ok=True)

# 處理過的影片目錄 - 從 Gait 系統的輸出目錄讀取
OUTPUT_VIDEOS_DIR = GAIT_DIR / "output" / "OutputVideos"
OUTPUT_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# 保留舊的目錄定義以備不時之需（用於 API 返回）
PROCESSED_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# 檔案大小限制 (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024


@router.post("/upload", response_model=RecognitionResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    上傳影片並進行 Gait 識別
    
    Args:
        file: 上傳的影片檔案
        
    Returns:
        RecognitionResponse: 處理過的影片 URL 和多個識別結果
    """
    # 驗證檔案類型
    file_extension = Path(file.filename).suffix.lower()
    if file_extension != '.mp4':
        raise HTTPException(
            status_code=400,
            detail=f"僅支援 .mp4 格式的影片檔案，您上傳的檔案格式為: {file_extension if file_extension else '未知格式'}"
        )
    
    # 生成 probe_id
    probe_id = f"probe_{uuid.uuid4().hex[:8]}"
    
    # 儲存上傳的檔案到正式版 Gait 系統的輸入目錄，固定命名為 probe_1.mp4
    saved_filename = "probe_1.mp4"
    saved_path = PROBE_INPUT_DIR / saved_filename
    
    # 如果已存在 probe_1.mp4，先刪除舊檔案
    if saved_path.exists():
        saved_path.unlink()
    
    try:
        # 讀取檔案內容並檢查大小
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"檔案大小超過限制 ({MAX_FILE_SIZE / 1024 / 1024}MB)"
            )
        
        # 儲存檔案
        with open(saved_path, "wb") as f:
            f.write(content)
        
        # 呼叫 Gait 系統處理
        try:
            processed_video_path, recognition_results = gait_service.process_video(str(saved_path), probe_id)
        except Exception as e:
            # 清理檔案
            if saved_path.exists():
                saved_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"Gait 處理失敗: {str(e)}"
            )
        
        # 檢查處理結果（允許空結果，用於測試）
        # if not recognition_results:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Gait 系統未回傳有效的識別結果"
        #     )
        
        # 從 Gait 系統的輸出目錄查找處理過的影片
        # 正式版 main.py 會將處理後的影片保存到 output/OutputVideos/{timestamp}/G-{gallery}_P-probe_1.mp4
        processed_path = None
        
        # 查找最新的輸出目錄（按時間戳排序）
        if OUTPUT_VIDEOS_DIR.exists():
            timestamp_dirs = sorted(
                [d for d in OUTPUT_VIDEOS_DIR.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # 在最新的時間戳目錄中查找處理過的影片
            for timestamp_dir in timestamp_dirs:
                # 查找格式為 G-*_P-probe_1.mp4 的檔案
                video_files = list(timestamp_dir.glob("G-*_P-probe_1.mp4"))
                if video_files:
                    processed_path = video_files[0]
                    break
        
        # 如果找不到處理過的影片，使用 process_video 返回的路徑
        if processed_path is None or not processed_path.exists():
            processed_path = Path(processed_video_path)
        
        # 將處理過的影片複製到 processed 目錄供 API 使用
        if processed_path.exists():
            processed_filename = f"{probe_id}_processed.mp4"
            target_path = PROCESSED_DIR / processed_filename
            shutil.copy2(str(processed_path), str(target_path))
            processed_video_path = str(target_path)
        
        # 生成處理過的影片 URL
        processed_video_url = f"/api/video/{probe_id}_processed.mp4"
        
        # 轉換識別結果為 PersonInfo 模型
        person_infos = []
        for result in recognition_results:
            # 確保有必要的欄位
            person_info = PersonInfo(
                gallery_id=result.get("gallery_id", ""),
                person_id=result.get("person_id", ""),
                name=result.get("name", "Unknown"),
                photo_url=result.get("photo_url") or result.get("photo"),
                Department=result.get("Department") or result.get("department"),
                Year_in_school=result.get("Year in school") or result.get("Year_in_school"),
            )
            person_infos.append(person_info)
        
        # 清理上傳的原始檔案
        if saved_path.exists():
            saved_path.unlink()
        
        # 回傳結果
        return RecognitionResponse(
            probe_id=probe_id,
            processed_video_url=processed_video_url,
            recognition_results=person_infos,
            total_detected=len(person_infos)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # 清理檔案
        if saved_path.exists():
            saved_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"處理過程中發生錯誤: {str(e)}"
        )


@router.get("/video/{filename}")
async def get_processed_video(filename: str):
    """
    取得處理過的影片檔案
    
    Args:
        filename: 影片檔案名稱
        
    Returns:
        FileResponse: 影片檔案
    """
    video_path = PROCESSED_DIR / filename
    
    if not video_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"找不到影片檔案: {filename}"
        )
    
    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=filename
    )




@router.get("/health")
async def health_check():
    """健康檢查 endpoint"""
    return {"status": "ok", "message": "服務運行中"}

