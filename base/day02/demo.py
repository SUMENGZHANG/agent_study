"""
Day 2 Demo — list, tuple, dict, set, 切片, 推导式
以及用字典表示营销标签及其元数据
"""

# ========== 1. 列表基础 ==========
print("=" * 40)
print("1. 列表（list）")
print("=" * 40)

fruits = ["apple", "banana", "cherry"]
print(f"原始列表: {fruits}")

fruits.append("orange")
print(f"添加 orange: {fruits}")

fruits.insert(1, "mango")
print(f"在索引1插入 mango: {fruits}")

fruits.remove("banana")
print(f"删除 banana: {fruits}")

popped = fruits.pop()
print(f"弹出最后一个: {popped}, 剩余: {fruits}")

print(f"cherry 在列表中: {'cherry' in fruits}")
print()

# ========== 2. 元组 ==========
print("=" * 40)
print("2. 元组（tuple）")
print("=" * 40)

point = (3, 4)
print(f"坐标: {point}")

x, y = point
print(f"解包: x={x}, y={y}")

# 交换变量
a, b = 10, 20
print(f"交换前: a={a}, b={b}")
a, b = b, a
print(f"交换后: a={a}, b={b}")
print()

# ========== 3. 字典 ==========
print("=" * 40)
print("3. 字典（dict）")
print("=" * 40)

user = {
    "name": "Alice",
    "age": 28,
    "city": "Shanghai"
}
print(f"用户: {user}")
print(f"姓名: {user['name']}")
print(f"邮箱（安全获取）: {user.get('email', 'N/A')}")

user["email"] = "alice@example.com"
print(f"添加邮箱后: {user}")

print("\n遍历字典:")
for key, value in user.items():
    print(f"  {key}: {value}")
print()

# ========== 4. 集合 ==========
print("=" * 40)
print("4. 集合（set）")
print("=" * 40)

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"集合 a: {a}")
print(f"集合 b: {b}")
print(f"并集: {a | b}")
print(f"交集: {a & b}")
print(f"差集 (a-b): {a - b}")
print()

# ========== 5. 切片 ==========
print("=" * 40)
print("5. 切片（Slicing）")
print("=" * 40)

nums = list(range(10))
print(f"原始: {nums}")
print(f"[2:5]  : {nums[2:5]}")
print(f"[:3]   : {nums[:3]}")
print(f"[7:]   : {nums[7:]}")
print(f"[::2]  : {nums[::2]}")
print(f"[::-1] : {nums[::-1]}")
print(f"[-3:]  : {nums[-3:]}")
print()

# ========== 6. 推导式 ==========
print("=" * 40)
print("6. 推导式（Comprehension）")
print("=" * 40)

squares = [x ** 2 for x in range(10)]
print(f"平方列表: {squares}")

evens = [x for x in range(20) if x % 2 == 0]
print(f"偶数列表: {evens}")

word_lengths = {w: len(w) for w in ["hello", "world", "python"]}
print(f"单词长度字典: {word_lengths}")

unique_lengths = {len(w) for w in ["hi", "hello", "hey", "world"]}
print(f"唯一长度集合: {unique_lengths}")
print()

# ========== 7. 营销标签示例 ==========
print("=" * 40)
print("7. 营销标签（dict 实战）")
print("=" * 40)

label = {
    "name": "high_value_user",
    "display_name": "高价值用户",
    "type": "behavior",
    "conditions": [
        {"field": "total_order_amount", "op": ">=", "value": 10000},
        {"field": "order_count", "op": ">=", "value": 5}
    ],
    "metadata": {
        "created_by": "marketing_team",
        "version": "1.0",
        "is_active": True
    }
}

print(f"标签名称: {label['display_name']}")
print(f"标签类型: {label['type']}")
print(f"创建者: {label['metadata']['created_by']}")

print("筛选条件:")
for i, cond in enumerate(label["conditions"]):
    print(f"  {i+1}. {cond['field']} {cond['op']} {cond['value']}")
