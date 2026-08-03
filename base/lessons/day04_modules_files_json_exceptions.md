# Day 4 — 模块、包、文件读写、JSON、异常捕获

> 日期：2026-07-24 | 预计用时：2 小时

---

## 1. Python 核心概念

### 1.1 模块（Module）

一个 `.py` 文件就是一个模块，可以用 `import` 引入：

```python
# math_utils.py
def add(a, b):
    return a + b

PI = 3.14159
```

```python
# 其他文件中导入
import math_utils                     # 导入整个模块
from math_utils import add, PI        # 导入指定内容
from math_utils import *              # 导入所有内容（不推荐）
import math_utils as mu               # 起别名
```

**内置常用模块：**

| 模块 | 用途 | 示例 |
|------|------|------|
| `os` | 操作系统接口 | `os.path.exists("file.txt")` |
| `sys` | 系统参数 | `sys.argv` 命令行参数 |
| `json` | JSON 处理 | `json.loads()`, `json.dumps()` |
| `datetime` | 日期时间 | `datetime.now()` |
| `random` | 随机数 | `random.randint(1, 10)` |
| `pathlib` | 路径操作（推荐） | `Path("data") / "file.json"` |

### 1.2 包（Package）

包就是包含 `__init__.py` 的目录，用于组织多个模块：

```
my_package/
├── __init__.py       # 标识这是一个包（可以为空）
├── utils.py
└── models/
    ├── __init__.py
    └── user.py
```

```python
from my_package.utils import add
from my_package.models.user import User
```

### 1.3 文件读写

使用 `with` 语句（上下文管理器）确保文件正确关闭：

```python
# 写文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
    f.write("第二行内容\n")

# 读文件（全部内容）
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 读文件（逐行）
with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 追加内容
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加的内容\n")
```

**文件打开模式：**

| 模式 | 含义 |
|------|------|
| `"r"` | 读取（默认） |
| `"w"` | 写入（覆盖） |
| `"a"` | 追加 |
| `"rb"` / `"wb"` | 二进制读/写 |
| `"r+"` | 读写 |

### 1.4 JSON

JSON（JavaScript Object Notation）是通用的数据交换格式，Python 通过 `json` 模块处理：

```python
import json

# Python 对象 → JSON 字符串
data = {"name": "Alice", "age": 28, "hobbies": ["reading", "coding"]}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON 字符串 → Python 对象
parsed = json.loads(json_str)
print(parsed["name"])

# 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

**Python ↔ JSON 类型映射：**

| Python | JSON |
|--------|------|
| `dict` | `{}` 对象 |
| `list`, `tuple` | `[]` 数组 |
| `str` | `"string"` |
| `int`, `float` | 数字 |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

### 1.5 异常捕获

```python
# 基本结构
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"除零错误：{e}")
except (TypeError, ValueError) as e:
    print(f"类型或值错误：{e}")
except Exception as e:
    print(f"其他错误：{e}")
else:
    print("没有异常时执行")
finally:
    print("无论如何都执行")
```

**常见异常类型：**

| 异常 | 触发场景 |
|------|---------|
| `ValueError` | `int("abc")` |
| `TypeError` | `"a" + 1` |
| `KeyError` | `dict["不存在的key"]` |
| `IndexError` | `list[100]` |
| `FileNotFoundError` | 打开不存在的文件 |
| `json.JSONDecodeError` | 解析格式错误的 JSON |
| `ZeroDivisionError` | `1 / 0` |

**主动抛出异常：**

```python
def validate_age(age):
    if age < 0 or age > 150:
        raise ValueError(f"年龄不合法：{age}")
    return age
```

**最佳实践：**
- 只捕获你知道的具体异常，不要裸 `except:`
- 用 `finally` 做资源清理
- 异常信息要有意义，便于调试

---

## 2. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| **模块导入** | `import math` 或 `from math import sqrt` | `import java.util.List;` |
| **包结构** | 目录 + `__init__.py` | 目录即包，无需额外文件 |
| **文件读写** | `with open() as f:` 一行搞定 | `try-with-resources` + `BufferedReader` |
| **JSON** | `json.loads()` / `json.dumps()` | `ObjectMapper` (Jackson) 或 `Gson` |
| **异常捕获** | `try/except/else/finally` | `try/catch/finally` |
| **自定义异常** | `class MyError(Exception): pass` | `class MyException extends Exception {}` |
| **抛出异常** | `raise ValueError("msg")` | `throw new IllegalArgumentException("msg")` |
| **异常基类** | `Exception` / `BaseException` | `Exception` / `Throwable` |
| **检查型异常** | Python 没有（所有异常都是运行时） | Java 有 checked exception，必须声明或捕获 |

### Java 程序员常犯的错误

```python
# ❌ Java 思维：过度捕获
try:
    do_something()
except Exception:
    pass  # 吞掉异常，出 bug 找不到原因

# ✅ Python 风格：捕获具体异常，给出有意义的处理
try:
    do_something()
except FileNotFoundError:
    print("配置文件不存在，使用默认配置")
except json.JSONDecodeError as e:
    print(f"配置文件格式错误：{e}")
```

---

## 3. 代码 Demo

运行 `day04/demo.py` 查看完整示例：

```bash
python base/day04/demo.py
```

核心功能：读取标签 JSON 文件，解析并处理缺失字段和格式错误。

---

## 4. 每日作业

### 作业 1：标签 JSON 读取器（必做）

项目目录 `base/day04/` 下有一个 `labels.json` 文件，包含多个营销标签定义。

**要求：**
1. 编写函数 `load_labels(filepath)` 读取并解析 JSON 文件
2. 处理文件不存在的情况（`FileNotFoundError`）
3. 处理 JSON 格式错误的情况（`json.JSONDecodeError`）
4. 编写函数 `validate_label(label)` 校验每个标签是否包含必需字段：`name`、`type`、`conditions`
5. 缺失字段时用 `dict.get()` 提供默认值，并打印警告
6. 编写函数 `print_labels(labels)` 格式化打印所有标签

### 作业 2：模块与包练习（必做）

1. 在 `day04/` 下创建一个 `utils.py`，包含一个 `safe_get(data, key, default)` 函数
2. 在 `demo.py` 或 `work.py` 中 `from day04.utils import safe_get` 使用它
3. 用这个函数安全地从标签字典中获取嵌套字段

### 作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. `import module` 和 `from module import func` 有什么区别？
2. 为什么推荐用 `with open()` 而不是直接 `open()`？
3. Python 和 Java 的异常体系有什么关键区别？（提示：checked vs unchecked）

---

## 5. 完成标准

- [ ] demo.py 能正常运行
- [ ] 作业 1、2 代码能运行并输出正确结果
- [ ] 能口述 3 个思考题的答案
