from __future__ import annotations
import threading
from typing import Optional
from models.online_trainer import online_update_loop


def start_online_worker(model_path: str, data_source: str) -> threading.Thread:
    t = threading.Thread(target=online_update_loop, args=(model_path, data_source), daemon=True)
    t.start()
    return t
