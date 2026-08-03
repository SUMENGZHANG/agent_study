# Day 6 — 命令行圈人条件生成器（argparse、CLI 结构、JSON 输出）

> 日期：2026-07-26 | 预计用时：2 小时

---

## 1. Python 核心概念

### 1.1 命令行参数基础

Python 程序可以从命令行接收参数，有三种方式：

```python
# 方式 1：sys.argv（原始方式）
import sys
print(sys.argv)       # ['demo.py', '--age', '25']
# argv[0] 是文件名，argv[1:] 是参数

# 方式 2：argparse（推荐，功能完整）
import argparse
parser = argparse.ArgumentParser(description="圈人条件生成器")
parser.add_argument("--age", type=int, help="年龄")
args = parser.parse_args()
print(args.age)       # 25

# 方式 3：click / typer（第三方库，更优雅，后面学）
```

### 1.2 argparse 详解

`argparse` 是 Python 内置的命令行参数解析模块，功能强大：

```python
import argparse

parser = argparse.ArgumentParser(
    description="圈人条件生成器",
    epilog="示例: python demo.py --age 25 --city hangzhou"
)

# 必选参数（位置参数）
parser.add_argument("name", help="标签名称")

# 可选参数（带 -- 前缀）
parser.add_argument("--age", type=int, default=18, help="年龄（默认18）")
parser.add_argument("--city", type=str, default="beijing", help="城市")
parser.add_argument("--vip", action="store_true", help="是否VIP")
parser.add_argument("--gender", choices=["male", "female"], help="性别")

# 解析
args = parser.parse_args()
print(args.name)     # 位置参数的值
print(args.age)      # 25（int 类型）
print(args.vip)      # True/False（布尔值）
```

**常用参数类型：**

| 写法 | 含义 |
|------|------|
| `type=int` | 自动转为整数 |
| `default=18` | 默认值 |
| `required=True` | 必填 |
| `choices=["a", "b"]` | 限定可选值 |
| `action="store_true"` | 布尔开关（出现即为 True） |
| `nargs="+"` | 接收多个值，返回列表 |
| `help="..."` | 帮助文本 |

**命令行使用示例：**

```bash
# 查看帮助
python demo.py --help

# 基本使用
python demo.py --age 25 --city hangzhou --vip

# 多个值
python demo.py --tags vip new_user high_value
```

### 1.3 `if __name__ == "__main__":` 模式

这是 Python 的标准入口模式，防止被 import 时自动执行：

```python
# my_module.py
def greet(name):
    return f"Hello, {name}"

# 直接运行才执行，被 import 时不执行
if __name__ == "__main__":
    print(greet("World"))
```

**为什么需要？**
- 直接运行 `python my_module.py` → `__name__` 是 `"__main__"`，会执行
- 被其他文件 `import my_module` → `__name__` 是 `"my_module"`，不执行

### 1.4 dataclass 与 JSON 互转

`dataclasses.asdict()` 可以把 dataclass 对象转为 dict，再用 `json.dumps()` 输出：

```python
from dataclasses import dataclass, asdict
import json

@dataclass
class Condition:
    field_name: str
    op: str
    value: int | float | str | bool

c = Condition("age", ">=", 18)

# dataclass → dict → JSON 字符串
d = asdict(c)                          # {'field_name': 'age', 'op': '>=', 'value': 18}
json_str = json.dumps(d, ensure_ascii=False, indent=2)
print(json_str)

# 批量转换
conditions = [Condition("age", ">=", 18), Condition("city", "==", "hangzhou")]
json_output = json.dumps([asdict(c) for c in conditions], ensure_ascii=False, indent=2)
```

### 1.5 标准 CLI 程序结构

一个规范的命令行程序通常这样组织：

```python
"""
命令行工具：XXX 生成器
用法：python xxx.py --param1 value1 --param2 value2
"""
import argparse
import json
from dataclasses import dataclass, asdict


# 1. 数据模型定义
@dataclass
class MyData:
    ...


# 2. 核心业务逻辑
def build_data(args) -> MyData:
    ...


# 3. 输出格式化
def format_output(data: MyData, fmt: str = "json") -> str:
    ...


# 4. 主函数
def main():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument(...)
    args = parser.parse_args()

    data = build_data(args)
    output = format_output(data)
    print(output)


# 5. 入口
if __name__ == "__main__":
    main()
```

---

## 2. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| **命令行参数** | `argparse`（内置） | `args[]` 数组 / `picocli` / `JCommander` |
| **参数解析** | `parser.parse_args()` 自动解析 | 手动解析 `args[]` 或用注解 |
| **帮助文档** | `--help` 自动生成 | 手写或框架生成 |
| **入口点** | `if __name__ == "__main__":` | `public static void main(String[] args)` |
| **JSON 输出** | `json.dumps(obj, indent=2)` | `ObjectMapper.writeValueAsString()` |
| **对象→字典** | `dataclasses.asdict()` | 反射 / Jackson 序列化 |

### Java 程序员常犯的错误

```python
# ❌ Java 思维：手动解析 sys.argv
import sys
age = None
for i, arg in enumerate(sys.argv):
    if arg == "--age" and i + 1 < len(sys.argv):
        age = int(sys.argv[i + 1])

# ✅ Python 风格：用 argparse，一行搞定
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--age", type=int, default=18)
args = parser.parse_args()
```

---

## 3. 代码 Demo

运行 `day06/demo.py` 查看完整示例：

```bash
# 查看帮助
python base/day06/demo.py --help

# 生成圈人条件
python base/day06/demo.py --age 25 --city hangzhou --gender male --vip

# 输出到文件
python base/day06/demo.py --age 30 --city shanghai -o output.json
```

核心功能：接收年龄、城市、性别、VIP 等参数，生成圈人条件并输出 JSON。

---

## 4. 每日作业

### 作业 1：命令行圈人条件生成器（必做）

编写一个 `audience_generator.py` 命令行工具：

**支持的参数：**
- `--min-age` / `--max-age`：年龄范围（int）
- `--gender`：性别，可选 `male` / `female`，非必填
- `--city`：城市，字符串，可传多个（`nargs="+"`）
- `--vip`：是否 VIP，布尔开关
- `--logic`：条件间逻辑，`AND`（默认）/ `OR`
- `-o` / `--output`：输出文件路径，不指定则打印到终端

**输出格式：** 标准 JSON，包含 `request_id`（用 uuid 生成）、`conditions` 列表和 `logic`。

**示例调用：**
```bash
python audience_generator.py --min-age 18 --max-age 35 --city hangzhou shanghai --vip --logic AND
```

### 作业 2：从 JSON 文件读取并合并条件（选做）

支持 `--label-file` 参数读取 Day 4 的 `labels.json`，将文件中的标签条件与命令行参数合并输出。

### 作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. `if __name__ == "__main__":` 的作用是什么？不加会怎样？
2. `argparse` 的 `action="store_true"` 和 `type=bool` 有什么区别？
3. Python 的 `json.dumps()` 和 Java 的 `ObjectMapper` 在使用上有什么不同？

---

## 5. 完成标准

- [ ] demo.py 能正常运行（`--help` 正常输出）
- [ ] 作业 1 的命令行工具能正确接收参数并输出 JSON
- [ ] 能口述 3 个思考题的答案
