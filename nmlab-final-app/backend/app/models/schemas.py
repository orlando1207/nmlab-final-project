"""
Pydantic 模型定義
"""
from pydantic import BaseModel
from typing import Optional


class PersonInfo(BaseModel):
    """個人資訊模型"""
    id: str
    name: str
    photo: str
    department: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[str] = None


class RecognitionResult(BaseModel):
    """識別結果模型"""
    probe_id: str
    gallery_id: str
    person_info: PersonInfo


class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    error: str
    detail: Optional[str] = None

