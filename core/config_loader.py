import os
import yaml
from typing import Any, Dict

DEFAULT_CONFIG = {
    "settings": {
        "timeout": 3.0,
        "threads": 10,
        "output_folder": "reports",
        "theme": "dark_hacker",
        "default_report_format": "json"
    }
}

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config if config else DEFAULT_CONFIG
    except Exception:
        return DEFAULT_CONFIG