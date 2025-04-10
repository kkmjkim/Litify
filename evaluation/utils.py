from functools import wraps
from pathlib import Path

import yaml


def get_project_path():
    project_path = Path(__file__).parents[1]
    return project_path


def load_config():
    with open(str(get_project_path() / 'conf.d' / 'config.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    return config


def load_prompt(template_name: str):
    prompt_path = get_project_path() / 'resource' / 'prompt' / template_name
    return read_text_file(prompt_path)


def ensure_absolute_path(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            path = Path(args[0])
            if not path.is_absolute():
                new_path = get_project_path() / path
                args = (new_path,) + args[1:]
        return func(*args, **kwargs)

    return wrapper


@ensure_absolute_path
def read_text_file(file_path):
    if file_path.exists() and file_path.is_file():
        with file_path.open(mode='r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        print(f"File '{file_path}' does not exist or is not a regular file.")
        return None
