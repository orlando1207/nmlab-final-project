"""
Gait 系統處理橋接層
負責調用 Gait 系統並處理結果
"""
import os
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 載入 identity_map.json
IDENTITY_MAP_PATH = Path(__file__).parent / "identity_map.json"
_identity_map: Optional[Dict] = None

def _load_identity_map() -> Dict:
    """載入 identity_map.json"""
    global _identity_map
    if _identity_map is not None:
        return _identity_map
    
    if not IDENTITY_MAP_PATH.exists():
        print(f"警告: 找不到 identity_map.json 於 {IDENTITY_MAP_PATH}")
        return {}
    
    with open(IDENTITY_MAP_PATH, 'r', encoding='utf-8') as f:
        _identity_map = json.load(f)
    
    return _identity_map


# 嘗試導入真實的 Gait 系統
USE_REAL_GAIT = False
_main_func = None

# 嘗試載入 gait/main.py 或 gait/demo/libs/main.py
_gait_main_paths = [
    Path(__file__).parent / "main.py",
    Path(__file__).parent / "demo" / "libs" / "main.py"
]

for main_path in _gait_main_paths:
    if main_path.exists():
        try:
            spec = importlib.util.spec_from_file_location("gait.main", main_path)
            if spec is not None and spec.loader is not None:
                gait_main_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(gait_main_module)
                
                # 嘗試找到 main 函數
                if hasattr(gait_main_module, "main"):
                    _main_func = gait_main_module.main
                    USE_REAL_GAIT = True
                    print(f"成功載入 Gait 系統: {main_path}")
                    break
        except Exception as e:
            print(f"警告: 無法導入 Gait 系統 ({main_path}): {str(e)}")

if not USE_REAL_GAIT:
    print("提示: 使用 Mock 模式")


def process_video(video_path: str, probe_id: str) -> Tuple[str, List[Dict]]:
    """
    處理影片並回傳處理過的影片路徑和識別結果
    
    Args:
        video_path: 輸入影片檔案路徑
        probe_id: Probe 識別碼
        
    Returns:
        tuple: (processed_video_path, recognition_results)
            - processed_video_path: 處理過的影片檔案路徑
            - recognition_results: 識別結果列表，每個元素包含個人資訊
    """
    # 檢查檔案是否存在
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"影片檔案不存在: {video_path}")
    
    # 檢查檔案格式
    if not video_path.lower().endswith('.mp4'):
        raise ValueError(f"不支援的檔案格式，僅支援 .mp4")
    
    if USE_REAL_GAIT and _main_func is not None:
        # 使用真實的 Gait 系統
        try:
            # 調用您的 Gait main.py 中的 main 函數
            # 預期回傳: (processed_video_path, recognition_dict)
            result = _main_func(video_path)
            
            # 處理回傳結果
            if isinstance(result, tuple) and len(result) == 2:
                processed_video_path, recognition_dict = result
            elif isinstance(result, dict):
                # 如果只回傳字典，假設處理過的影片在同一位置
                recognition_dict = result
                processed_video_path = video_path  # 使用原影片
            else:
                raise ValueError(f"Gait main 函數回傳格式不正確: {type(result)}")
            
            # 使用 identity_map 映射識別結果
            identity_map = _load_identity_map()
            recognition_results = _map_recognition_results(recognition_dict, identity_map)
            
            return processed_video_path, recognition_results
            
        except Exception as e:
            raise RuntimeError(f"Gait 處理失敗: {str(e)}") from e
    else:
        # Mock 模式：用於測試
        import time
        import shutil
        
        time.sleep(0.5)  # 模擬處理時間
        
        # Mock: 複製原影片作為處理過的影片
        processed_video_path = video_path.replace('.mp4', '_processed.mp4')
        shutil.copy2(video_path, processed_video_path)
        
        # Mock: 隨機選擇一些識別結果
        import random
        identity_map = _load_identity_map()
        gallery_keys = list(identity_map.keys())[:3]  # 取前3個 gallery
        
        recognition_results = []
        for gallery_key in random.sample(gallery_keys, min(2, len(gallery_keys))):
            person_id = random.choice(list(identity_map[gallery_key].keys()))
            person_info = identity_map[gallery_key][person_id]
            recognition_results.append({
                "gallery_id": gallery_key,
                "person_id": person_id,
                **person_info
            })
        
        return processed_video_path, recognition_results


def _map_recognition_results(recognition_dict: Dict, identity_map: Dict) -> List[Dict]:
    """
    將識別結果字典映射到個人資訊
    
    Args:
        recognition_dict: Gait 系統回傳的識別結果字典
            格式可能是: {"gallery_1": "001", "gallery_2": "002"} 
            或: {"001": "gallery_1", "002": "gallery_2"}
        identity_map: identity_map.json 的內容
        
    Returns:
        List[Dict]: 包含個人資訊的列表
    """
    results = []
    
    for key, value in recognition_dict.items():
        # 情況 1: key 是 gallery_id, value 是 person_id
        if key.startswith("gallery_") and key in identity_map:
            gallery_id = key
            person_id = str(value)
            if person_id in identity_map[gallery_id]:
                person_info = identity_map[gallery_id][person_id].copy()
                person_info["gallery_id"] = gallery_id
                person_info["person_id"] = person_id
                results.append(person_info)
        
        # 情況 2: value 是 gallery_id, key 是 person_id
        elif str(value).startswith("gallery_") and str(value) in identity_map:
            gallery_id = str(value)
            person_id = str(key)
            if person_id in identity_map[gallery_id]:
                person_info = identity_map[gallery_id][person_id].copy()
                person_info["gallery_id"] = gallery_id
                person_info["person_id"] = person_id
                results.append(person_info)
        
        # 情況 3: 嘗試直接查找
        else:
            # 遍歷所有 gallery 尋找匹配
            for gallery_id, persons in identity_map.items():
                if str(key) in persons:
                    person_info = persons[str(key)].copy()
                    person_info["gallery_id"] = gallery_id
                    person_info["person_id"] = str(key)
                    results.append(person_info)
                    break
    
    return results

