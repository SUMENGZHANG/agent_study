# Day 1 — 变量、数字、布尔值、字符串、输入输出

> 日期：2026-07-21 | 预计用时：2 小时

---

## 1. Python 核心概念

### 1.1 变量与类型

Python 是**动态类型**语言，变量不需要声明类型，赋值即创建：

```python
name = "Alice"      # str（字符串）
age = 25            # int（整数）
height = 1.68       # float（浮点数）
is_student = True   # bool（布尔值）
```

**关键特性：**
- 变量只是"标签"，贴在一个内存对象上，同一个变量可以先后指向不同类型的对象
- 用 `type()` 查看变量当前类型
- 用 `isinstance()` 判断是否为某种类型

### 1.2 数字（Number）

| 类型 | 说明 | 示例 |
|------|------|------|
| `int` | 整数，无长度限制 | `42`, `-7`, `10**100` |
| `float` | 双精度浮点数 | `3.14`, `1e-5` |
| `complex` | 复数（了解即可） | `3 + 4j` |

常用运算：

```python
a = 10
b = 3
print(a + b)    # 13  加
print(a - b)    # 7   减
print(a * b)    # 30  乘
print(a / b)    # 3.333…  除（永远返回 float）
print(a // b)   # 3   整除（地板除）
print(a % b)    # 1   取余
print(a ** b)   # 1000 幂运算
```

### 1.3 布尔值（Boolean）

只有两个值：`True` 和 `False`（首字母大写）。

**Falsy 值**（等价于 `False`）：`0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`

**Truthy 值**（等价于 `True`）：除上面以外的一切非空值

```python
bool(0)        # False
bool("")       # False
bool("hello")  # True
bool([1, 2])   # True
```

### 1.4 字符串（String）

字符串是**不可变**的字符序列，支持单引号、双引号和三引号：

```python
s1 = 'hello'
s2 = "world"
s3 = """这是
多行字符串"""
```

常用操作：

```python
name = "Python"
len(name)           # 6，长度
name.upper()        # "PYTHON"
name.lower()        # "python"
name.strip()        # 去首尾空白
name.replace("P", "J")  # "Jython"
name.split("t")     # ['Py', 'hon']
name[0]             # 'P'，索引
name[1:4]           # 'yth'，切片
f"I love {name}"    # f-string 格式化
```

**f-string**（推荐格式化方式）：

```python
price = 9.9
qty = 3
print(f"总价：{price * qty:.2f} 元")  # 总价：29.70 元
```

### 1.5 输入与输出

```python
# 输出
print("Hello", "World", sep="-", end="\n")  # Hello-World

# 输入（永远返回字符串）
name = input("请输入你的名字：")
age = int(input("请输入年龄："))  # 需要手动转类型
```

### 1.6 类型转换

```python
int("42")       # 42
float("3.14")   # 3.14
str(100)        # "100"
bool(1)         # True
```

转换失败会抛出 `ValueError`：

```python
int("abc")      # ValueError!
```

---

## 2. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| **变量声明** | `x = 10`（无需声明类型） | `int x = 10;`（必须声明类型） |
| **类型检查** | 运行时检查（动态类型） | 编译时检查（静态类型） |
| **字符串** | 不可变，支持 f-string `f"Hi {name}"` | 不可变，用 `+` 拼接或 `String.format()` |
| **布尔值** | `True` / `False` | `true` / `false` |
| **类型转换** | `int("42")` 函数式 | `Integer.parseInt("42")` 方法式 |
| **空值** | `None`（不是 0，不是 False） | `null` |
| **除法** | `10 / 3` → `3.333…`（真除） | `10 / 3` → `3`（整数除法） |
| **整除** | `10 // 3` → `3` | `10 / 3` → `3`（两者都是 int 时） |
| **幂运算** | `2 ** 10` → `1024` | `Math.pow(2, 10)` → `1024.0` |
| **大整数** | 自动支持，无上限 | 需要 `BigInteger` / `BigDecimal` |
| **输入** | `input()` 一行搞定 | 需要 `Scanner` 或 `BufferedReader` |
| **代码块** | 缩进（4 空格） | 花括号 `{}` |
| **语句结尾** | 不需要分号 | 必须分号 `;` |

### Java 程序员常犯的错误

```python
# ❌ Java 思维
int x = 10;          # SyntaxError
if (x > 5) { ... }  # Python 不用括号和花括号

# ✅ Python 风格
x = 10
if x > 5:
    print("大于5")
```

---

## 3. 代码 Demo

运行 `day01/demo.py` 查看完整示例：

```bash
python base/day01/demo.py
```

核心代码预览：

```python
# 温度转换：华氏度 → 摄氏度
fahrenheit = float(input("请输入华氏度："))
celsius = (fahrenheit - 32) * 5 / 9
print(f"{fahrenheit}°F = {celsius:.2f}°C")

# 字符串处理
text = "  Hello, Python World!  "
print(f"原始：'{text}'")
print(f"去空白：'{text.strip()}'")
print(f"大写：'{text.strip().upper()}'")
print(f"单词数：{len(text.split())}")
```

---

## 4. 每日作业

### 作业 1：温度转换器（必做）

编写一个程序，要求用户输入摄氏度，输出对应的华氏度和开尔文温度。

公式：
- 华氏度 = 摄氏度 × 9/5 + 32
- 开尔文 = 摄氏度 + 273.15

**要求：**
- 使用 `input()` 接收输入
- 使用 f-string 格式化输出，保留 1 位小数
- 处理非法输入（用 `try/except`）

### 作业 2：个人名片生成器（必做）

编写程序，让用户依次输入：姓名、年龄、身高（米）、职业。
然后输出一张格式化的"个人名片"：

```
========== 个人名片 ==========
姓名：张三
年龄：28 岁
身高：1.75 米
职业：工程师
==============================
```

**要求：**
- 用变量存储所有信息
- 用 f-string 对齐输出
- 计算并显示出生年份（用当前年份减年龄）

### 作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. Python 的 `None` 和 Java 的 `null` 有什么区别？
2. 为什么 Python 的 `10 / 3` 结果是 `3.333…` 而不是 `3`？
3. Python 变量和 Java 变量在本质上有什么不同？（提示：标签 vs 盒子）

---

## 5. 完成标准

- [ ] demo.py 能正常运行
- [ ] 作业 1、2 代码能运行并输出正确结果
- [ ] 能口述 3 个思考题的答案
