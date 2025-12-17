"""
API 路由定義
"""
import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from app.models.schemas import RecognitionResult, ErrorResponse
from app.services.gait_service import GaitService
from app.services.person_service import PersonService

router = APIRouter(prefix="/api", tags=["gait"])

# 初始化服務
gait_service = GaitService()
person_service = PersonService()

# 上傳目錄
UPLOAD_DIR = Path(__file__).parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 檔案大小限制 (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024


@router.post("/upload", response_model=RecognitionResult)
async def upload_video(file: UploadFile = File(...)):
    """
    上傳影片並進行 Gait 識別
    
    Args:
        file: 上傳的影片檔案
        
    Returns:
        RecognitionResult: 識別結果與個人資訊
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
            gait_result = gait_service.process_video(str(saved_path), probe_id)
        except Exception as e:
            # 清理檔案
            if saved_path.exists():
                saved_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"Gait 處理失敗: {str(e)}"
            )
        
        # 取得 gallery_id
        gallery_id = gait_result.get(probe_id)
        if not gallery_id:
            raise HTTPException(
                status_code=500,
                detail="Gait 系統未回傳有效的識別結果"
            )
        
        # 取得個人資訊
        person_info = person_service.get_person_info(gallery_id)
        if not person_info:
            raise HTTPException(
                status_code=404,
                detail=f"找不到 gallery_id {gallery_id} 對應的個人資訊"
            )
        
        # 清理上傳的檔案
        if saved_path.exists():
            saved_path.unlink()
        
        # 回傳結果
        return RecognitionResult(
            probe_id=probe_id,
            gallery_id=gallery_id,
            person_info=person_info
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


@router.get("/person/{person_id}", response_model=dict)
async def get_person_info(person_id: str):
    """
    取得個人資訊
    
    Args:
        person_id: Gallery ID
        
    Returns:
        dict: 個人資訊
    """
    person_info = person_service.get_person_info(person_id)
    
    if not person_info:
        raise HTTPException(
            status_code=404,
            detail=f"找不到 ID {person_id} 對應的個人資訊"
        )
    
    return person_info.dict()


@router.get("/health")
async def health_check():
    """健康檢查 endpoint"""
    return {"status": "ok", "message": "服務運行中"}

