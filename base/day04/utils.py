from typing import Any

from my_package import utils


def util_use(name:str):
    return utils.safe_get(name)


def safe_get(data: dict, key: str, default: Any = None):
    return None