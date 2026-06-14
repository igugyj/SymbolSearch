import json
from pathlib import Path

import sys

DEFAULT_HOTKEY = "Ctrl+Alt+S"


def get_config_path():
    return Path(sys.argv[0]).resolve().parent / "config.json"


def load_config():
    path = get_config_path()
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"hotkey": DEFAULT_HOTKEY}


def save_config(data: dict):
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
