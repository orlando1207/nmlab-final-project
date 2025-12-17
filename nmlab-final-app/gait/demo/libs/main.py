"""
Gait 識別系統主程式（測試用）
簡化版本，直接輸出不需要真的處理
隨機從 identity_map 選擇人員作為識別結果
"""
import os
import json
import shutil
import time
import random
from pathlib import Path
from typing import Tuple, Dict


def _load_identity_map() -> Dict:
    """載入 identity_map.json"""
    identity_map_path = Path("./identity_map.json")
    if not identity_map_path.exists():
        print(f"[測試模式] 警告: 找不到 identity_map.json 於 {identity_map_path}")
        return {}
    
    with open(identity_map_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main() -> None:
    """
    處理影片並進行步態識別（測試用簡化版本）
    
    正式版會從 InputVideos/probe/probe_1.mp4 讀取
    輸出到 output/OutputVideos/{timestamp}/G-{gallery}_P-probe_1.mp4
    並保存識別結果到 recognition_result.json
    """
    # 輸入路徑
    probe_input_path = Path("./InputVideos/probe/probe_1.mp4")
    
    if not probe_input_path.exists():
        raise FileNotFoundError(f"找不到輸入影片: {probe_input_path}")
    
    # 載入 identity_map
    identity_map = _load_identity_map()
    
    # 創建輸出目錄
    output_dir = Path("./output/OutputVideos/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 創建時間戳目錄
    current_time = time.localtime()
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    timestamp_dir = output_dir / timestamp
    timestamp_dir.mkdir(parents=True, exist_ok=True)
    
    # 隨機選擇一個 gallery 和人員（用於測試）
    gallery_name = "gallery_1"  # 默認值
    recognition_dict = {}  # 格式: {gallery_id: person_id}
    
    if identity_map:
        # 隨機選擇一個 gallery
        gallery_keys = list(identity_map.keys())
        if gallery_keys:
            selected_gallery = random.choice(gallery_keys)
            gallery_name = selected_gallery.replace("gallery_", "gallery")
            
            # 從選中的 gallery 中隨機選擇 1-2 個人
            person_ids = list(identity_map[selected_gallery].keys())
            if person_ids:
                num_persons = min(random.randint(1, 2), len(person_ids))
                selected_persons = random.sample(person_ids, num_persons)
                
                # 構建識別結果字典（格式: {gallery_id: person_id}）
                # 如果有多個人，可以有多個條目，但這裡簡化為只選第一個
                recognition_dict[selected_gallery] = selected_persons[0]
                
                print(f"[測試模式] 隨機選擇: {selected_gallery} -> {selected_persons[0]}")
    
    # 生成輸出文件名（模擬正式版格式）
    output_filename = f"G-{gallery_name}_P-probe_1.mp4"
    output_path = timestamp_dir / output_filename
    
    # 直接複製輸入影片到輸出位置（測試用，不需要真的處理）
    shutil.copy2(str(probe_input_path), str(output_path))
    
    # 保存識別結果到 JSON 文件（供 process.py 讀取）
    recognition_result_path = timestamp_dir / "recognition_result.json"
    with open(recognition_result_path, 'w', encoding='utf-8') as f:
        json.dump(recognition_dict, f, ensure_ascii=False, indent=2)
    
    print(f"[測試模式] 影片已輸出到: {output_path}")
    print(f"[測試模式] 識別結果已保存到: {recognition_result_path}")
    print(f"[測試模式] 識別結果: {recognition_dict}")


# 測試用
if __name__ == "__main__":
    main()

