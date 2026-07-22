"""
Day 1 Demo — 变量、数字、布尔值、字符串、输入输出
运行方式：python base/day01/demo.py
"""

# ============================================================
# 1. 变量与类型
# ============================================================
name = "Alice"
age = 25
height = 1.68
is_student = True

print("--- 变量与类型 ---")
print(f"名字：{name}，类型：{type(name)}")
print(f"年龄：{age}，类型：{type(age)}")
print(f"身高：{height}，类型：{type(height)}")
print(f"是学生：{is_student}，类型：{type(is_student)}")

# 变量可以改变类型（动态类型）
x = 10
print(f"\nx = {x}，类型：{type(x)}")
x = "now I'm a string"
print(f"x = {x}，类型：{type(x)}")


# ============================================================
# 2. 数字运算
# ============================================================
print("\n--- 数字运算 ---")
a, b = 10, 3
print(f"{a} + {b} = {a + b}")       # 13
print(f"{a} - {b} = {a - b}")       # 7
print(f"{a} * {b} = {a * b}")       # 30
print(f"{a} / {b} = {a / b}")       # 3.333...（真除，永远 float）
print(f"{a} // {b} = {a // b}")     # 3（整除/地板除）
print(f"{a} % {b} = {a % b}")       # 1（取余）
print(f"{a} ** {b} = {a ** b}")     # 1000（幂运算）

# Python 大整数无上限（Java 需要 BigInteger）
big = 2 ** 100
print(f"\n2 ** 100 = {big}")


# ============================================================
# 3. 布尔值与 Truthy / Falsy
# ============================================================
print("\n--- 布尔值 ---")
print(f"bool(0)      = {bool(0)}")         # False
print(f"bool(0.0)    = {bool(0.0)}")       # False
print(f'bool("")     = {bool("")}')        # False
print(f'bool("hi")   = {bool("hi")}')     # True
print(f"bool([1])    = {bool([1])}")      # True
print(f"bool(None)   = {bool(None)}")     # False

# isinstance 判断类型
print(f"\nisinstance(42, int)     = {isinstance(42, int)}")     # True
print(f'isinstance("hi", str)   = {isinstance("hi", str)}')   # True


# ============================================================
# 4. 字符串操作
# ============================================================
print("\n--- 字符串操作 ---")
s = "  Hello, Python World!  "
print(f"原始字符串：'{s}'")
print(f"strip()   ：'{s.strip()}'")
print(f"upper()   ：'{s.strip().upper()}'")
print(f"lower()   ：'{s.strip().lower()}'")
print(f"replace() ：'{s.strip().replace('Python', 'Java')}'")
print(f"split()   ：{s.split()}")
print(f"len()     ：{len(s)}")

# 索引和切片
word = "Python"
print(f"\n字符串：'{word}'")
print(f"word[0]    = '{word[0]}'")     # P
print(f"word[-1]   = '{word[-1]}'")    # n
print(f"word[1:4]  = '{word[1:4]}'")   # yth
print(f"word[:3]   = '{word[:3]}'")    # Pyt
print(f"word[3:]   = '{word[3:]}'")  # hon

# f-string 格式化
print("\n--- f-string 格式化 ---")
price = 9.9
qty = 3
print(f"单价：{price} 元，数量：{qty}，总价：{price * qty:.2f} 元")
print(f"百分比：{0.856:.1%}")           # 85.6%
print(f"补零：{42:05d}")               # 00042
print(f"左对齐：|{'hi':<10}|")         # |hi        |
print(f"右对齐：|{'hi':>10}|")         # |        hi|
print(f"居中  ：|{'hi':^10}|")         # |    hi    |


# ============================================================
# 5. 输入与输出
# ============================================================
print("\n--- 输入输出 Demo ---")
print("Hello", "World", sep=" - ", end="!\n")  # Hello - World!

# 取消注释以下代码可练习输入：
# user_name = input("请输入你的名字：")
# user_age = int(input("请输入年龄："))
# print(f"你好 {user_name}，你 {user_age} 岁了！")


# ============================================================
# 6. 类型转换
# ============================================================
print("\n--- 类型转换 ---")
print(f'int("42")    = {int("42")}')
print(f'float("3.14") = {float("3.14")}')
print(f'str(100)     = {repr(str(100))}')
print(f"bool(1)      = {bool(1)}")
print(f"bool(0)      = {bool(0)}")

# 转换失败
try:
    result = int("abc")
except ValueError as e:
    print(f'int("abc") 失败：{e}')


# ============================================================
# 7. 温度转换示例（华氏度 → 摄氏度）
# ============================================================
print("\n--- 温度转换 ---")
fahrenheit = 100.0  # 直接赋值，无需 input
celsius = (fahrenheit - 32) * 5 / 9
kelvin = celsius + 273.15
print(f"{fahrenheit}°F = {celsius:.2f}°C = {kelvin:.2f}K")


# ============================================================
# 8. 字符串综合练习
# ============================================================
print("\n--- 字符串综合练习 ---")
text = "  Hello, Python World!  "
stripped = text.strip()
print(f"原始      ：'{text}'")
print(f"去空白    ：'{stripped}'")
print(f"大写      ：'{stripped.upper()}'")
print(f"单词数量  ：{len(stripped.split())}")
print(f"字符数量  ：{len(stripped)}")
print(f"是否以 H 开头：{stripped.startswith('H')}")
print(f"World 位置：{stripped.find('World')}")
