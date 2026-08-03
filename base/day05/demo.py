"""
Day 5 Demo — class、对象、继承、dataclass、类型注解
用 dataclass 定义 Condition、Label、AudienceRequest 数据模型
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


# ========== 1. 用 dataclass 定义数据模型 ==========
print("=" * 50)
print("1. dataclass 定义数据模型")
print("=" * 50)


class LabelType(Enum):
    """标签类型枚举"""
    BEHAVIOR = "behavior"
    ATTRIBUTE = "attribute"
    PREFERENCE = "preference"


@dataclass
class Condition:
    """圈人条件"""
    field_name: str
    op: str
    value: int | float | str | bool

    def describe(self) -> str:
        return f"{self.field_name} {self.op} {self.value}"


@dataclass
class Label:
    """营销标签"""
    name: str
    display_name: str
    label_type: str
    conditions: list[Condition] = field(default_factory=list)

    def validate(self) -> bool:
        """校验标签是否合法"""
        if not self.name:
            print(f"  ✗ 标签 name 不能为空")
            return False
        if not self.conditions:
            print(f"  ⚠ 标签 '{self.name}' 没有条件")
            return False
        return True

    def condition_count(self) -> int:
        return len(self.conditions)


# 创建对象
c1 = Condition("total_order_amount", ">=", 10000)
c2 = Condition("order_count", ">=", 5)
label = Label("high_value_user", "高价值用户", "behavior", [c1, c2])

print(f"标签：{label}")
print(f"条件数：{label.condition_count()}")
print(f"条件描述：{[c.describe() for c in label.conditions]}")
print(f"校验结果：{label.validate()}")
print()


# ========== 2. AudienceRequest 圈人请求 ==========
print("=" * 50)
print("2. AudienceRequest 圈人请求")
print("=" * 50)


@dataclass
class AudienceRequest:
    """圈人请求"""
    request_id: str
    labels: list[Label] = field(default_factory=list)
    logic: str = "AND"  # AND / OR

    def summary(self) -> str:
        label_names = [f"'{lb.display_name}'" for lb in self.labels]
        logic_text = " 且 " if self.logic == "AND" else " 或 "
        return f"圈人请求 [{self.request_id}]：{logic_text.join(label_names)}"

    def validate(self) -> bool:
        if not self.request_id:
            print("  ✗ request_id 不能为空")
            return False
        if not self.labels:
            print("  ✗ 至少需要一个标签")
            return False
        for lb in self.labels:
            if not lb.validate():
                return False
        return True


# 组装圈人请求
c3 = Condition("register_days", "<=", 30)
new_user_label = Label("new_user", "新注册用户", "attribute", [c3])

request = AudienceRequest(
    request_id="REQ-001",
    labels=[label, new_user_label],
    logic="AND",
)
print(request.summary())
print(f"校验：{request.validate()}")
print()


# ========== 3. 继承与多态 ==========
print("=" * 50)
print("3. 继承与多态")
print("=" * 50)


class ConditionMatcher:
    """条件匹配器基类"""
    def match(self, user_tags: dict, condition: Condition) -> bool:
        raise NotImplementedError("子类必须实现 match()")


class SimpleMatcher(ConditionMatcher):
    """简单比较匹配器"""
    def match(self, user_tags: dict, condition: Condition) -> bool:
        tag_value = user_tags.get(condition.field_name)
        if tag_value is None:
            return False
        ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            ">":  lambda a, b: a > b,
            "<":  lambda a, b: a < b,
        }
        op_func = ops.get(condition.op)
        if op_func is None:
            raise ValueError(f"不支持的操作符: {condition.op}")
        return op_func(tag_value, condition.value)


class FuzzyMatcher(ConditionMatcher):
    """模糊匹配器（字符串包含）"""
    def match(self, user_tags: dict, condition: Condition) -> bool:
        tag_value = user_tags.get(condition.field_name)
        if tag_value is None:
            return False
        return str(condition.value).lower() in str(tag_value).lower()


# 多态演示
matcher1 = SimpleMatcher()
matcher2 = FuzzyMatcher()

user = {"age": 25, "city": "hangzhou", "total_order_amount": 12000}
cond_age = Condition("age", ">=", 18)
cond_city = Condition("city", "==", "hang")

print(f"SimpleMatcher - age >= 18: {matcher1.match(user, cond_age)}")
print(f"SimpleMatcher - city == hang: {matcher1.match(user, cond_city)}")
print(f"FuzzyMatcher  - city 包含 hang: {matcher2.match(user, cond_city)}")
print()


# ========== 4. 从 JSON 构建 dataclass 对象 ==========
print("=" * 50)
print("4. 从 JSON 构建 dataclass 对象")
print("=" * 50)


def parse_condition(data: dict) -> Condition:
    """将 JSON dict 转为 Condition 对象"""
    return Condition(
        field_name=data.get("field", "unknown"),
        op=data.get("op", "=="),
        value=data.get("value", 0),
    )


def parse_label(data: dict) -> Label:
    """将 JSON dict 转为 Label 对象"""
    conditions = [parse_condition(c) for c in data.get("conditions", [])]
    return Label(
        name=data.get("name", "unknown"),
        display_name=data.get("display_name", "未命名"),
        label_type=data.get("type", "unclassified"),
        conditions=conditions,
    )


# 读取 Day 4 的 labels.json
labels_file = Path(__file__).parent.parent / "day04" / "labels.json"
with open(labels_file, "r", encoding="utf-8") as f:
    raw_labels = json.load(f)

# 转为 Label 对象列表
label_objects = [parse_label(item) for item in raw_labels]

print(f"从 JSON 加载了 {len(label_objects)} 个标签对象\n")
for lb in label_objects:
    valid = "✓" if lb.validate() else "✗"
    print(f"  [{valid}] {lb.display_name} ({lb.name}) - {lb.condition_count()} 个条件")

print()

# 用加载的对象构建圈人请求
valid_labels = [lb for lb in label_objects if lb.validate()]
auto_request = AudienceRequest(
    request_id="REQ-AUTO",
    labels=valid_labels,
    logic="OR",
)
print(f"\n自动组装：{auto_request.summary()}")
