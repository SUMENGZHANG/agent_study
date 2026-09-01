"""TODO: 实现下面两个函数，使 work.py 的断言全部通过。"""

ALLOWED_OPS = (">=", "<=", "==")


def validate_age_range(min_age: int | None, max_age: int | None) -> None:
    """
    要求：
    1. 两个参数都允许为 None（表示不限制该方向）
    2. 出现的具体年龄不能为负数
    3. 两者都指定时，必须 min_age <= max_age
    4. 违反任一条抛 ValueError，错误信息要说明是哪个参数出了问题
    """
    raise NotImplementedError("请实现 validate_age_range")


def build_condition_dict(field_name: str, op: str, value: int | float | str | bool) -> dict:
    """
    要求：
    1. op 必须在 ALLOWED_OPS 中，否则抛 ValueError
    2. field_name 不能为空字符串，否则抛 ValueError
    3. 返回 {"field_name": ..., "op": ..., "value": ...}
    """
    raise NotImplementedError("请实现 build_condition_dict")
