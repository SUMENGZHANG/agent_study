"""
Day 03 笔记：控制流、函数、参数与作用域

今日目标：
1. 掌握 if / elif / else 分支
2. 掌握 for 循环和 while 循环
3. 掌握函数定义、参数、返回值
4. 理解作用域（局部变量 vs 全局变量）
5. 实现“根据标签条件筛选用户”的函数
"""

# ----------------------
# 1. if / elif / else
# ----------------------
age = 25

if age < 13:
    category = "儿童"
elif age < 20:
    category = "青少年"
elif age < 60:
    category = "成年人"
else:
    category = "老年人"

print(f"年龄 {age} 属于：{category}")

# ----------------------
# 2. for 循环
# ----------------------
users = ["Alice", "Bob", "Carol"]
for user in users:
    print(user)

# 需要索引时用 enumerate
for index, user in enumerate(users, start=1):
    print(f"{index}. {user}")

# range 生成数字序列
for i in range(3):
    print(i)  # 0, 1, 2

# ----------------------
# 3. while 循环
# ----------------------
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1

# ----------------------
# 4. 函数定义、参数、返回值
# ----------------------
def greet(name: str) -> str:
    """打招呼函数。"""
    return f"Hello, {name}!"


message = greet("Sumeng")
print(message)


# 默认参数
def create_user(name: str, age: int = 18) -> dict:
    return {"name": name, "age": age}


print(create_user("Tom"))
print(create_user("Jerry", age=22))


# 可变参数 *args 接收多余的位置参数
def sum_numbers(*numbers: int) -> int:
    total = 0
    for n in numbers:
        total += n
    return total


print(sum_numbers(1, 2, 3, 4))


# 可变关键字参数 **kwargs 接收多余的关键字参数
def print_info(**kwargs: str) -> None:
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_info(name="Sumeng", city="Hangzhou")

# ----------------------
# 5. 作用域
# ----------------------
GLOBAL_VALUE = 100  # 全局变量，习惯用大写


def demo_scope() -> None:
    local_value = 10  # 局部变量，只在函数内有效
    print(f"函数内：local_value={local_value}, GLOBAL_VALUE={GLOBAL_VALUE}")


demo_scope()
# print(local_value)  # 报错！函数外访问不到

# 如果要在函数里修改全局变量，用 global
counter = 0


def increment() -> None:
    global counter
    counter += 1


increment()
increment()
print(f"counter = {counter}")
