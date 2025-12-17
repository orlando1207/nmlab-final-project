"""
Pydantic 模型定義
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class PersonInfo(BaseModel):
    """個人資訊模型"""
    gallery_id: str
    person_id: str
    name: str
    photo_url: Optional[str] = None
    Department: Optional[str] = None
    Year_in_school: Optional[str] = None
    # 保留舊欄位以向後兼容
    id: Optional[str] = None
    photo: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[str] = None


class RecognitionResult(BaseModel):
    """識別結果模型（單一結果，向後兼容）"""
    probe_id: str
    gallery_id: str
    person_info: PersonInfo


class RecognitionResponse(BaseModel):
    """完整的識別回應模型（支援多個結果和處理過的影片）"""
    probe_id: str
    processed_video_url: str  # 處理過的影片 URL
    recognition_results: List[PersonInfo]  # 多個識別結果
    total_detected: int  # 檢測到的人數


class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    error: str
    detail: Optional[str] = None

