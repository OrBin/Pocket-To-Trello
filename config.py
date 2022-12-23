import json
from os.path import dirname, abspath
from pathlib import Path
from typing import Dict, Any


CONFIG_FILE_NAME = Path(dirname(abspath(__file__))) / 'config' / 'config.json'
AUTH_DATA_KEY = 'authentication'


def load_config() -> Dict[str, Any]:
    with open(CONFIG_FILE_NAME, 'r') as conf_file:
        conf_data = json.load(conf_file)
    return conf_data
