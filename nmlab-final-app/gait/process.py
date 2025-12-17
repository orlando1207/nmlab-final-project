"""
Gait 系統處理橋接層
負責調用 Gait 系統並處理結果
"""
import os
import json
import inspect
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
            # 檢查 main 函數的簽名
            sig = inspect.signature(_main_func)
            param_count = len(sig.parameters)
            
            # 保存當前工作目錄
            original_cwd = os.getcwd()
            gait_dir = Path(__file__).parent
            
            try:
                # 切換到 gait 目錄（正式版 main.py 使用相對路徑）
                os.chdir(str(gait_dir))
                
                # 根據參數數量調用 main 函數
                if param_count == 0:
                    # 正式版 main() 無參數，直接從 InputVideos/probe/probe_1.mp4 讀取
                    # 視頻應該已經由 routes.py 保存到正確位置
                    result = _main_func()
                else:
                    # 舊版 main(video_path) 有參數
                    result = _main_func(video_path)
                
                # 處理回傳結果
                recognition_dict = {}
                if isinstance(result, tuple) and len(result) == 2:
                    processed_video_path, recognition_dict = result
                elif isinstance(result, dict):
                    # 如果只回傳字典
                    recognition_dict = result
                    processed_video_path = None
                elif result is None:
                    # 正式版 main() 不返回值，需要從輸出目錄讀取
                    processed_video_path = None
                else:
                    raise ValueError(f"Gait main 函數回傳格式不正確: {type(result)}")
                
                # 如果 main() 不返回處理後的視頻路徑，從輸出目錄查找
                if processed_video_path is None:
                    output_dir = gait_dir / "output" / "OutputVideos"
                    latest_timestamp_dir = None
                    
                    if output_dir.exists():
                        # 查找最新的時間戳目錄
                        timestamp_dirs = sorted(
                            [d for d in output_dir.iterdir() if d.is_dir()],
                            key=lambda x: x.stat().st_mtime,
                            reverse=True
                        )
                        # 在最新的時間戳目錄中查找處理過的影片
                        for timestamp_dir in timestamp_dirs:
                            video_files = list(timestamp_dir.glob("G-*_P-probe_1.mp4"))
                            if video_files:
                                processed_video_path = str(video_files[0])
                                latest_timestamp_dir = timestamp_dir
                                break
                    
                    # 如果還是找不到，使用原視頻路徑
                    if processed_video_path is None:
                        processed_video_path = video_path
                    
                    # 如果 main() 沒有返回識別結果，嘗試從輸出目錄讀取 recognition_result.json
                    if not recognition_dict and latest_timestamp_dir is not None:
                        recognition_result_file = latest_timestamp_dir / "recognition_result.json"
                        if recognition_result_file.exists():
                            try:
                                with open(recognition_result_file, 'r', encoding='utf-8') as f:
                                    recognition_dict = json.load(f)
                                print(f"[測試模式] 從文件讀取識別結果: {recognition_dict}")
                            except Exception as e:
                                print(f"[測試模式] 讀取識別結果文件失敗: {str(e)}")
                
                # 使用 identity_map 映射識別結果
                identity_map = _load_identity_map()
                if recognition_dict:
                    recognition_results = _map_recognition_results(recognition_dict, identity_map)
                else:
                    # 如果沒有識別結果，返回空列表
                    recognition_results = []
                
                return processed_video_path, recognition_results
                
            finally:
                # 恢復原始工作目錄
                os.chdir(original_cwd)
            
        except Exception as e:
            raise RuntimeError(f"Gait 處理失敗: {str(e)}") from e
    else:
        # Mock 模式：模擬正式版流程，用於測試
        import time
        import shutil
        from datetime import datetime
        
        # 保存當前工作目錄
        original_cwd = os.getcwd()
        gait_dir = Path(__file__).parent
        
        try:
            # 切換到 gait 目錄（模擬正式版的行為）
            os.chdir(str(gait_dir))
            
            # 模擬處理時間
            time.sleep(1)  # 模擬處理時間
            
            # 模擬正式版：從 InputVideos/probe/probe_1.mp4 讀取
            probe_input_path = gait_dir / "InputVideos" / "probe" / "probe_1.mp4"
            
            if not probe_input_path.exists():
                raise FileNotFoundError(f"找不到輸入影片: {probe_input_path}")
            
            # 模擬正式版：創建輸出目錄結構 output/OutputVideos/{timestamp}/
            output_dir = gait_dir / "output" / "OutputVideos"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 創建時間戳目錄（模擬正式版的行為）
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y_%m_%d_%H_%M_%S")
            timestamp_dir = output_dir / timestamp
            timestamp_dir.mkdir(parents=True, exist_ok=True)
            
            # 模擬正式版：生成處理後的影片文件名 G-{gallery}_P-probe_1.mp4
            # 隨機選擇一個 gallery 來模擬
            import random
            identity_map = _load_identity_map()
            gallery_keys = list(identity_map.keys())
            
            # 選擇一個 gallery（如果有的話）
            selected_gallery = None
            gallery_name = "gallery_1"  # 默認值
            
            if gallery_keys:
                # 隨機選擇一個 gallery
                selected_gallery = random.choice(gallery_keys)
                gallery_name = selected_gallery.replace("gallery_", "gallery")
            
            # 生成處理後的影片文件名（模擬正式版格式）
            processed_filename = f"G-{gallery_name}_P-probe_1.mp4"
            processed_video_path = timestamp_dir / processed_filename
            
            # 複製原影片作為處理過的影片（模擬處理結果）
            shutil.copy2(str(probe_input_path), str(processed_video_path))
            
            print(f"[Mock] 模擬處理完成，輸出影片: {processed_video_path}")
            
            # 生成假的識別結果（模擬正式版返回的結果）
            recognition_results = []
            
            if selected_gallery and selected_gallery in identity_map:
                # 從選中的 gallery 中隨機選擇 1-2 個人
                person_ids = list(identity_map[selected_gallery].keys())
                if person_ids:
                    num_persons = min(random.randint(1, 2), len(person_ids))
                    selected_persons = random.sample(person_ids, num_persons)
                    
                    for person_id in selected_persons:
                        person_info = identity_map[selected_gallery][person_id].copy()
                        recognition_results.append({
                            "gallery_id": selected_gallery,
                            "person_id": person_id,
                            **person_info
                        })
            
            # 如果沒有識別結果，創建一個假的結果用於測試
            if not recognition_results:
                recognition_results = [{
                    "gallery_id": "gallery_1",
                    "person_id": "001",
                    "name": "測試人員",
                    "Department": "測試系",
                    "Year_in_school": "測試年級",
                    "photo_url": ""
                }]
                print("[Mock] 使用默認測試識別結果")
            
            # 返回處理後的影片路徑（絕對路徑）
            return str(processed_video_path.absolute()), recognition_results
                
        finally:
            # 恢復原始工作目錄
            os.chdir(original_cwd)


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

