# Day 5 — class、对象、继承、dataclass、类型注解

> 日期：2026-07-25 | 预计用时：2 小时

---

## 1. Python 核心概念

### 1.1 类与对象（Class & Object）

类是蓝图，对象是实例。Python 用 `class` 关键字定义类：

```python
class Dog:
    # 类属性（所有实例共享）
    species = "犬科"

    # 构造方法：创建对象时自动调用
    def __init__(self, name: str, age: int):
        self.name = name      # 实例属性
        self.age = age

    # 实例方法
    def bark(self) -> str:
        return f"{self.name} 说：汪汪！"

    # 打印对象时的友好展示
    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, age={self.age})"


# 创建对象
dog1 = Dog("旺财", 3)
dog2 = Dog("小白", 5)
print(dog1.bark())         # 旺财 说：汪汪！
print(dog2)                # Dog(name='小白', age=5)
```

**关键概念：**
- `self` — 代表实例本身（类似 Java 的 `this`，但必须显式写出）
- `__init__` — 构造方法（类似 Java 的构造器）
- `__repr__` — 定义对象的"官方"字符串表示（调试用）
- `__str__` — 定义对象的"友好"字符串表示（给用户看）

### 1.2 继承（Inheritance）

子类继承父类的属性和方法，可以重写或扩展：

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError("子类必须实现 speak()")


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name}：喵~"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name}：汪！"


# 多态：同一个方法，不同表现
animals = [Cat("咪咪"), Dog("旺财")]
for animal in animals:
    print(animal.speak())
```

**常用内置基类：**

| 基类 | 用途 |
|------|------|
| `Exception` | 自定义异常 |
| `Enum` | 枚举类型 |
| `ABC`（from abc） | 抽象基类，强制子类实现方法 |

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2
```

### 1.3 dataclass（数据类）

`dataclass` 是 Python 3.7+ 引入的装饰器，自动生成 `__init__`、`__repr__`、`__eq__` 等方法，非常适合做数据模型：

```python
from dataclasses import dataclass, field

@dataclass
class Condition:
    field_name: str
    op: str
    value: int | float | str | bool

@dataclass
class Label:
    name: str
    display_name: str
    label_type: str
    conditions: list[Condition] = field(default_factory=list)

    def condition_count(self) -> int:
        return len(self.conditions)


# 使用
c1 = Condition("age", ">=", 18)
c2 = Condition("city", "==", "hangzhou")
label = Label("adult_hz", "杭州成年人", "attribute", [c1, c2])
print(label)                    # Label(name='adult_hz', ...)
print(label.condition_count())  # 2
```

**dataclass vs 普通 class：**

| 特性 | 普通 class | @dataclass |
|------|-----------|------------|
| `__init__` | 手写 | 自动生成 |
| `__repr__` | 手写 | 自动生成 |
| `__eq__` | 手写 | 自动生成 |
| `__hash__` | 默认有 | 需要 `frozen=True` |
| 适用场景 | 有复杂逻辑 | 数据载体/DTO |

**dataclass 常用参数：**

```python
@dataclass(frozen=True)   # 不可变（类似 Java record）
@dataclass(order=True)     # 自动生成 __lt__, __gt__ 等比较方法
@dataclass(slots=True)     # Python 3.10+，节省内存
```

### 1.4 类型注解（Type Hints）

类型注解让代码更可读、IDE 更智能，但**运行时不强制检查**：

```python
# 基本类型
name: str = "Alice"
age: int = 28
price: float = 9.99
is_vip: bool = True

# 容器类型
scores: list[int] = [90, 85, 78]
config: dict[str, str] = {"host": "localhost", "port": "8080"}
unique_ids: set[int] = {1, 2, 3}

# 可选类型（可能为 None）
email: str | None = None          # Python 3.10+ 写法
from typing import Optional
email: Optional[str] = None       # 旧写法

# 联合类型
value: int | str = "hello"        # 可以是 int 或 str

# 函数类型注解
def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! " * times).strip()

# Any 类型（尽量避免使用）
from typing import Any
def process(data: Any) -> None:
    print(data)
```

**复杂类型注解：**

```python
from typing import Callable

# 函数作为参数
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# 嵌套容器
users: list[dict[str, Any]] = [
    {"name": "Alice", "age": 28},
    {"name": "Bob", "age": 35},
]
```

### 1.5 枚举（Enum）

```python
from enum import Enum

class LabelType(Enum):
    BEHAVIOR = "behavior"
    ATTRIBUTE = "attribute"
    PREFERENCE = "preference"

# 使用
label_type = LabelType.BEHAVIOR
print(label_type.value)   # behavior
print(label_type.name)    # BEHAVIOR

# 遍历
for t in LabelType:
    print(t.name, "=", t.value)
```

---

## 2. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| **定义类** | `class Dog:` | `public class Dog {}` |
| **构造方法** | `def __init__(self, name):` | `public Dog(String name) {}` |
| **this** | `self`（必须显式写） | `this`（可省略） |
| **继承** | `class Cat(Animal):` | `class Cat extends Animal {}` |
| **多继承** | 支持 `class C(A, B):` | 不支持（只能 `implements` 多接口） |
| **访问控制** | 约定 `_` 私有、`__` 名称改写 | `private/protected/public` 关键字 |
| **接口/抽象类** | `ABC` + `@abstractmethod` | `interface` / `abstract class` |
| **数据类** | `@dataclass` | `record`（Java 16+）或 Lombok `@Data` |
| **类型检查** | 类型注解（运行时不强制） | 强类型（编译时强制） |
| **枚举** | `class Color(Enum):` | `enum Color {}` |
| **对象比较** | `__eq__` 方法 | `equals()` 方法 |
| **字符串表示** | `__repr__` / `__str__` | `toString()` |

### Java 程序员常犯的错误

```python
# ❌ Java 思维：给所有东西都写 getter/setter
class User:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

# ✅ Python 风格：直接访问属性，需要时用 @property
class User:
    def __init__(self, name: str):
        self.name = name

# 或者需要校验时用 @property
class User:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("名字不能为空")
        self._name = value
```

```python
# ❌ Java 思维：过度使用继承
class BaseService: ...
class UserService(BaseService): ...
class OrderService(BaseService): ...

# ✅ Python 风格：优先用组合和 Mixin，保持简单
# dataclass 做数据模型，普通 class 做行为封装
```

---

## 3. 代码 Demo

运行 `day05/demo.py` 查看完整示例：

```bash
python base/day05/demo.py
```

核心功能：用 `dataclass` 定义 Condition、Label、AudienceRequest 数据模型，实现标签的创建、校验和圈人请求组装。

---

## 4. 每日作业

### 作业 1：数据模型定义（必做）

用 `dataclass` 定义以下三个数据模型：

1. **Condition** — 圈人条件
   - `field_name: str` — 字段名（如 "age"）
   - `op: str` — 操作符（如 ">="）
   - `value: int | float | str | bool` — 目标值

2. **Label** — 营销标签
   - `name: str` — 英文标识
   - `display_name: str` — 中文显示名
   - `label_type: str` — 标签类型
   - `conditions: list[Condition]` — 条件列表
   - 实现方法 `validate()` 校验 name 和 conditions 不为空

3. **AudienceRequest** — 圈人请求
   - `request_id: str` — 请求 ID
   - `labels: list[Label]` — 使用的标签
   - `logic: str` — 标签间逻辑（"AND" / "OR"），默认 "AND"
   - 实现方法 `summary()` 打印请求摘要

### 作业 2：从 JSON 构建对象（必做）

读取 Day 4 的 `labels.json` 文件，将每个 JSON 字典转为 `Label` 对象，并用 `AudienceRequest` 组装一个完整的圈人请求。

### 作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. `@dataclass` 和普通 class 什么时候该用哪个？
2. Python 的 `self` 和 Java 的 `this` 有什么区别？
3. Python 的类型注解和 Java 的类型系统有什么本质不同？（提示：运行时 vs 编译时）

---

## 5. 完成标准

- [ ] demo.py 能正常运行
- [ ] 作业 1、2 代码能运行并输出正确结果
- [ ] 能口述 3 个思考题的答案
