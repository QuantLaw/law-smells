import json
import os
from typing import List

import regex as re


def get_files(path: str, expression: str = "", full_path: bool = False) -> List[str]:
    if full_path:
        return [
            f"{path}/{f}" for f in sorted(os.listdir(path)) if re.search(expression, f)
        ]
    else:
        return [f for f in sorted(os.listdir(path)) if re.search(expression, f)]


def load_json(file: str) -> dict:
    with open(file) as f:
        result = json.load(f)
    return result


def get_txt(path: str) -> str:
    with open(path) as f:
        text = f.read()
    return text
