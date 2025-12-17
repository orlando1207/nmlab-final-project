"""
個人資訊服務
處理 JSON 映射檔的讀取與查詢
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from app.models.schemas import PersonInfo


class PersonService:
    """個人資訊服務類別"""
    
    def __init__(self, json_path: str = None):
        """
        初始化服務
        
        Args:
            json_path: JSON 檔案路徑，預設為 data/person_info.json
        """
        if json_path is None:
            # 取得專案根目錄
            current_dir = Path(__file__).parent.parent.parent
            json_path = current_dir / "data" / "person_info.json"
        
        self.json_path = Path(json_path)
        self._person_data: Dict[str, Any] = {}
        self._load_data()
    
    def _load_data(self):
        """載入 JSON 資料"""
        if not self.json_path.exists():
            raise FileNotFoundError(f"個人資訊 JSON 檔案不存在: {self.json_path}")
        
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self._person_data = json.load(f)
    
    def get_person_info(self, gallery_id: str) -> Optional[PersonInfo]:
        """
        根據 gallery_id 取得個人資訊
        
        Args:
            gallery_id: Gallery 識別碼
            
        Returns:
            PersonInfo 物件，如果找不到則回傳 None
        """
        person_data = self._person_data.get(gallery_id)
        
        if person_data is None:
            return None
        
        return PersonInfo(**person_data)
    
    def reload_data(self):
        """重新載入 JSON 資料"""
        self._load_data()
    
    def get_all_person_ids(self) -> list:
        """取得所有個人 ID 列表"""
        return list(self._person_data.keys())

