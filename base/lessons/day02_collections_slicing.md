# Day 2 — list、tuple、dict、set、切片与推导式

> 日期：2026-07-22 | 预计用时：2 小时

---

## 1. Python 核心概念

### 1.1 列表（list）

有序、可变、可重复的元素集合，用 `[]` 创建：

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]  # 可以混合类型（但通常不推荐）
```

常用操作：

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")      # 末尾添加
fruits.insert(1, "mango")    # 指定位置插入
fruits.remove("banana")      # 删除第一个匹配值
fruits.pop()                 # 弹出并返回最后一个元素
fruits.pop(0)                # 弹出并返回指定索引元素
len(fruits)                  # 长度
"apple" in fruits            # 是否包含（True/False）
fruits.sort()                # 原地排序
fruits.reverse()             # 原地反转
fruits.index("cherry")       # 查找索引
fruits.count("apple")        # 计数
```

### 1.2 元组（tuple）

有序、**不可变**、可重复，用 `()` 创建：

```python
point = (3, 4)
colors = ("red", "green", "blue")
single = (42,)   # 注意：单元素元组必须加逗号
```

关键特性：
- 不可变 → 可以作为 `dict` 的 key
- 常用于**函数返回多个值**、**不可变的数据记录**
- 支持解包：`x, y = point`

```python
# 交换变量（Python 独有写法）
a, b = 1, 2
a, b = b, a   # a=2, b=1
```

### 1.3 字典（dict）

键值对集合，用 `{}` 创建，**键必须可哈希**（不可变类型）：

```python
user = {
    "name": "Alice",
    "age": 28,
    "hobbies": ["reading", "coding"]
}
```

常用操作：

```python
user["name"]                 # 获取值（键不存在则 KeyError）
user.get("email", "N/A")    # 安全获取（键不存在返回默认值）
user["email"] = "a@b.com"   # 新增/修改
del user["age"]              # 删除
"name" in user               # 是否包含键（True）
user.keys()                  # 所有键
user.values()                # 所有值
user.items()                 # 所有键值对
user.update({"age": 29})    # 批量更新
```

遍历字典：

```python
for key, value in user.items():
    print(f"{key}: {value}")
```

### 1.4 集合（set）

无序、**不可重复**，用 `{}` 创建：

```python
tags = {"vip", "new_user", "high_value"}
empty_set = set()   # 注意：{} 是空字典，set() 才是空集合
```

常用操作：

```python
a = {1, 2, 3}
b = {2, 3, 4}
a | b    # 并集：{1, 2, 3, 4}
a & b    # 交集：{2, 3}
a - b    # 差集：{1}
a ^ b    # 对称差集：{1, 4}
a.add(5)         # 添加
a.discard(1)     # 删除（不存在不报错）
a.remove(2)      # 删除（不存在则 KeyError）
```

### 1.5 切片（Slicing）

对序列（list、tuple、str）取子集的统一语法：`[start:stop:step]`

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
nums[2:5]      # [2, 3, 4]       从索引2到4（不含5）
nums[:3]       # [0, 1, 2]       前3个
nums[7:]       # [7, 8, 9]       从索引7到末尾
nums[::2]      # [0, 2, 4, 6, 8] 步长为2
nums[::-1]     # [9, 8, ..., 0]  反转
nums[-3:]      # [7, 8, 9]       最后3个
```

### 1.6 推导式（Comprehension）

用一行代码快速生成 list / dict / set：

```python
# 列表推导式
squares = [x ** 2 for x in range(10)]           # [0, 1, 4, 9, ..., 81]
evens = [x for x in range(20) if x % 2 == 0]    # 过滤偶数

# 字典推导式
word_lengths = {w: len(w) for w in ["hello", "world", "python"]}

# 集合推导式
unique_lengths = {len(w) for w in ["hi", "hello", "hey"]}  # {2, 5, 3}
```

---

## 2. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| **列表** | `nums = [1, 2, 3]` | `List<Integer> nums = new ArrayList<>(Arrays.asList(1,2,3));` |
| **元组** | `point = (3, 4)` | 无原生支持，需 `Pair` 或 `record` |
| **字典** | `d = {"a": 1}` | `Map<String, Integer> d = new HashMap<>();` |
| **集合** | `s = {1, 2, 3}` | `Set<Integer> s = new HashSet<>(Arrays.asList(1,2,3));` |
| **切片** | `nums[1:4]` | 需要 `subList(1, 4)` 或手动循环 |
| **推导式** | `[x*2 for x in nums]` | 需要 `stream().map().collect()` |
| **解包** | `a, b, c = [1, 2, 3]` | 不支持，需逐个赋值 |
| **可变性** | list 可变，tuple 不可变 | ArrayList 可变，List.of() 不可变 |
| **泛型** | 不需要，动态类型 | 必须声明泛型 `<String, Integer>` |
| **初始化** | `[]`, `{}`, `()` 一行搞定 | 需要 `new` + 构造函数或工厂方法 |

### Java 程序员常犯的错误

```python
# ❌ Java 思维
nums = list()          # 虽然能跑，但 Pythonic 写法是 []
d = dict()             # Pythonic 写法是 {}
for i in range(len(nums)):   # C 风格循环
    print(nums[i])

# ✅ Python 风格
nums = []
d = {}
for item in nums:            # 直接遍历元素
    print(item)

# 需要索引时用 enumerate
for i, item in enumerate(nums):
    print(f"{i}: {item}")
```

---

## 3. 代码 Demo

运行 `day02/demo.py` 查看完整示例：

```bash
python base/day02/demo.py
```

核心代码预览：

```python
# 营销标签示例
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
```

---

## 4. 每日作业

### 作业 1：标签管理器（必做）

用 dict 和 list 实现一个简易营销标签管理系统：

1. 定义至少 3 个标签（用 dict 表示，包含 name、type、description）
2. 将所有标签存入一个 list
3. 写一个函数，按 `type` 筛选标签并打印
4. 写一个函数，查找某个 name 的标签并返回
5. 用推导式生成一个只包含标签 name 的列表

**要求：**
- 使用 `dict.get()` 安全访问字段
- 使用 f-string 格式化输出
- 使用 `for...in` 遍历和 `enumerate`

### 作业 2：数据分析小练习（必做）

给定以下数据：

```python
scores = [85, 92, 78, 95, 88, 76, 90, 83, 97, 72]
```

完成以下操作：
1. 用切片取出前 3 个和后 3 个成绩
2. 用推导式筛选出 90 分以上的成绩
3. 计算平均分（用 `sum()` 和 `len()`）
4. 用推导式生成一个 dict：`{索引: 成绩}` 只包含及格（>=60）的成绩
5. 将成绩转为 set 去重，再转回 list 排序

### 作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. list 和 tuple 有什么区别？什么时候该用哪个？
2. dict 的 key 为什么必须是不可变类型？（提示：哈希）
3. Python 的 set 和 Java 的 HashSet 在底层实现上有什么共同点？

---

## 5. 完成标准

- [ ] demo.py 能正常运行
- [ ] 作业 1、2 代码能运行并输出正确结果
- [ ] 能口述 3 个思考题的答案
