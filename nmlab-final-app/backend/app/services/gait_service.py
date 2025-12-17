"""
Gait 系統整合服務
負責呼叫 Gait 系統進行影片處理
"""
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Optional

# 計算 gait 模組路徑
project_root = Path(__file__).parent.parent.parent.parent
gait_process_path = project_root / "gait" / "process.py"

# 快取導入的模組
_gait_process_module: Optional[object] = None


def _load_gait_module():
    """動態載入 gait.process 模組"""
    global _gait_process_module
    
    if _gait_process_module is not None:
        return _gait_process_module
    
    if not gait_process_path.exists():
        raise FileNotFoundError(
            f"找不到 Gait 處理模組: {gait_process_path}\n"
            f"請確認 gait/process.py 檔案存在"
        )
    
    # 使用 importlib 動態載入模組
    spec = importlib.util.spec_from_file_location("gait.process", gait_process_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入 Gait 處理模組: {gait_process_path}")
    
    _gait_process_module = importlib.util.module_from_spec(spec)
    sys.modules["gait.process"] = _gait_process_module
    spec.loader.exec_module(_gait_process_module)
    
    return _gait_process_module


class GaitService:
    """Gait 系統服務類別"""
    
    @staticmethod
    def process_video(video_path: str, probe_id: str) -> Dict[str, str]:
        """
        處理影片並回傳識別結果
        
        Args:
            video_path: 影片檔案路徑
            probe_id: Probe 識別碼
            
        Returns:
            dict: {probe_id: gallery_id} 格式的識別結果
        """
        try:
            # 動態載入模組
            gait_module = _load_gait_module()
            
            # 調用 process_video 函數
            process_video_func = getattr(gait_module, "process_video")
            result = process_video_func(video_path, probe_id)
            
            return result
        except FileNotFoundError as e:
            raise RuntimeError(f"Gait 模組載入失敗: {str(e)}") from e
        except AttributeError as e:
            raise RuntimeError(
                f"Gait 模組中找不到 process_video 函數: {str(e)}\n"
                f"請確認 gait/process.py 中有定義 process_video 函數"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Gait 處理失敗: {str(e)}") from e

