import json
from pathlib import Path
from mau.config_models import MAUConfig

def load_config(config_path: str):
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    with open(path, "r") as f:
        config_dict = json.load(f)
    return MAUConfig.parse_obj(config_dict).dict()
