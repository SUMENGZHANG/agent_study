"""
Day 03 Demo：用函数实现“根据标签条件筛选用户”
"""
from typing import Any


# 一些示例用户，每人带有一组标签
USERS = [
    {"user_id": "u001", "name": "Alice", "tags": {"age": 25, "city": "hangzhou", "vip": True}},
    {"user_id": "u002", "name": "Bob", "tags": {"age": 17, "city": "shanghai", "vip": False}},
    {"user_id": "u003", "name": "Carol", "tags": {"age": 32, "city": "hangzhou", "vip": True}},
    {"user_id": "u004", "name": "David", "tags": {"age": 45, "city": "beijing", "vip": False}},
]


def get_tag(user: dict, tag_name: str) -> Any:
    """安全获取用户的某个标签值。"""
    return user.get("tags", {}).get(tag_name)


def match_condition(user: dict, condition: dict) -> bool:
    """
    判断单个用户是否满足一个条件。
    condition 示例：{"tag": "age", "op": ">=", "value": 18}
    """
    tag_value = get_tag(user, condition["tag"])
    if tag_value is None:
        return False

    op = condition["op"]
    target = condition["value"]

    if op == "==":
        return tag_value == target
    elif op == "!=":
        return tag_value != target
    elif op == ">":
        return tag_value > target
    elif op == ">=":
        return tag_value >= target
    elif op == "<":
        return tag_value < target
    elif op == "<=":
        return tag_value <= target
    elif op == "in":
        return target in tag_value
    else:
        raise ValueError(f"不支持的操作符：{op}")


def filter_users(users: list[dict], conditions: list[dict]) -> list[dict]:
    """根据多个条件筛选用户，所有条件需同时满足（AND 关系）。"""
    result = []
    for user in users:
        matched = True
        for condition in conditions:
            if not match_condition(user, condition):
                matched = False
                break
        if matched:
            result.append(user)
    return result


if __name__ == "__main__":
    # 筛选：杭州且 VIP 的用户
    conditions = [
        {"tag": "city", "op": "==", "value": "hangzhou"},
        {"tag": "vip", "op": "==", "value": True},
    ]
    matched = filter_users(USERS, conditions)
    print("杭州 VIP 用户：")
    for user in matched:
        print(f"  {user['name']} ({user['user_id']})")

    # 筛选：成年人（age >= 18）
    adult_conditions = [{"tag": "age", "op": ">=", "value": 18}]
    adults = filter_users(USERS, adult_conditions)
    print(f"\n成年人数量：{len(adults)}")
