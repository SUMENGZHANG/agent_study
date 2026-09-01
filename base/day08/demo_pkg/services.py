"""包内的业务逻辑模块：包内引用同包模块，用相对导入。"""

from .models import Condition  # 相对导入：同包内只认模块名，不依赖 sys.path


def build_age_condition(min_age: int) -> Condition:
    return Condition("age", ">=", min_age)


def summarize(conditions: list[Condition], logic: str = "AND") -> str:
    connector = f" {logic} "
    return connector.join(c.describe() for c in conditions)
