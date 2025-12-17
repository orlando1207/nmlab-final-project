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

# 上傳目錄
UPLOAD_DIR = Path(__file__).parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 處理過的影片目錄
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
    if not file.filename.lower().endswith('.mp4'):
        raise HTTPException(
            status_code=400,
            detail="僅支援 .mp4 格式的影片檔案"
        )
    
    # 生成 probe_id
    probe_id = f"probe_{uuid.uuid4().hex[:8]}"
    
    # 儲存上傳的檔案
    file_extension = Path(file.filename).suffix
    saved_filename = f"{probe_id}{file_extension}"
    saved_path = UPLOAD_DIR / saved_filename
    
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
        
        # 檢查處理結果
        if not recognition_results:
            raise HTTPException(
                status_code=500,
                detail="Gait 系統未回傳有效的識別結果"
            )
        
        # 將處理過的影片移動到 processed 目錄
        processed_path = Path(processed_video_path)
        if processed_path.exists():
            # 如果處理過的影片不在 processed 目錄，移動它
            if processed_path.parent != PROCESSED_DIR:
                processed_filename = f"{probe_id}_processed{processed_path.suffix}"
                target_path = PROCESSED_DIR / processed_filename
                shutil.move(str(processed_path), str(target_path))
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

