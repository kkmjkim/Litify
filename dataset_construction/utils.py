from pathlib import Path

import yaml


def get_project_path():
    project_path = Path(__file__).parents[1]
    return project_path


def load_config():
    with open(str(get_project_path() / 'conf.d' / 'config.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    return config