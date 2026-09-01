"""包内的数据模型模块。"""

from dataclasses import dataclass


@dataclass
class Condition:
    """圈人条件。"""

    field_name: str
    op: str
    value: int | float | str | bool

    def describe(self) -> str:
        return f"{self.field_name} {self.op} {self.value}"
