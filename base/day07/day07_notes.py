23"""
Day 7 语法复盘速查笔记

凭记忆写出本周（Day 1–6）学过的所有核心语法。
写完后再翻回各天笔记对照，查漏补缺。
"""


# ==================== Day 1：变量、数字、字符串、IO ====================

# 变量是标签，不是盒子
name = "Alice"
age = 25
height = 1.68
is_student = True

# 数字运算
# TODO: 写出 /、//、%、** 各一个示例

base_value = 10

base_value = base_value/3
print(base_value)

base_value = base_value//3

print(base_value)

base_value = base_value%3

# 布尔 Falsy 值
# TODO: 列出 5 个 Falsy 值


# f-string 格式化
# TODO: 用 f-string 输出 "Alice 今年 25 岁，身高 1.68 米"，身高保留 2 位小数
print(f"{name} 今年 {age} 岁，身高 {height:.2f} 米")
# 字符串操作
# TODO: 写出 strip、split、upper、replace、len 各一个用法
name.strip()
print(name)
split_name = name.split("i")[0]
print(split_name)
print(name.upper())
print(name.replace("Alice", "Bob"))

print(len(name))




# input（永远返回 str）
# TODO: 写一个接收年龄输入并转为 int 的代码
age = int(input("输入年龄："))


# 类型转换
# TODO: 写出 int()、float()、str()、bool() 各一个示例




# ==================== Day 2：集合、切片、推导式 ====================

# list
# TODO: 创建列表，写出 append、insert、pop、remove、sort 各一个用法
my_list = [1,2,3]

my_list.append(3)
my_list.insert(0,-1)
my_list.pop()

my_list.remove(2)
my_list.sort()

print(my_list)


# tuple
# TODO: 创建元组，写出解包写法，单元素元组怎么写
my_tuple = (1, 2, 3)
print(my_tuple)
single_tuple = (1,)
print(single_tuple)

# 解包：把元组的元素直接赋给多个变量
x, y, z = my_tuple    # x=1, y=2, z=3
print(x, y, z)

# 实际应用：交换两个变量（Java 需要临时变量 temp）
a, b = 1, 2
a, b = b, a            # a=2, b=1






# dict
# TODO: 创建字典，写出 get、items、keys、values、update 各一个用法


# set
# TODO: 创建集合，写出并集、交集、差集、add、discard


# 切片 [start:stop:step]
# TODO: 对一个列表写出 5 种不同切片写法


# 推导式
# TODO: 写出列表推导式、字典推导式、集合推导式各一个



# ==================== Day 3：控制流、函数、作用域 ====================

# if / elif / else
# TODO: 写一个三段条件判断


# for 循环
# TODO: 写出 for...in、enumerate、range 三种写法


# while 循环
# TODO: 写一个 while 循环


# 函数
# TODO: 定义一个带类型注解、默认参数、*args、**kwargs 的函数


# 作用域
# TODO: 解释局部变量和全局变量的区别，global 关键字怎么用



# ==================== Day 4：模块、文件、JSON、异常 ====================

# import 四种方式
# TODO: 写出四种 import 写法


# 文件读写
# TODO: 用 with open 写出读、写、追加三种模式


# JSON
# TODO: 写出 loads、dumps、load、dump 各一个用法


# 异常捕获
# TODO: 写出 try/except/else/finally 完整结构，捕获两种具体异常


# raise
# TODO: 写一个主动抛出 ValueError 的函数



# ==================== Day 5：类、dataclass、类型注解 ====================

# 普通 class
# TODO: 定义一个 class，包含 __init__、__repr__、一个实例方法


# 继承
# TODO: 写一个父类和子类的继承示例


# @dataclass
# TODO: 用 @dataclass 定义一个数据类，包含 field(default_factory=...)


# 类型注解
# TODO: 写出基本类型、容器类型、Optional、Union、函数类型注解



# ==================== Day 6：argparse、CLI、JSON 输出 ====================

# argparse 基本用法
# TODO: 创建一个 ArgumentParser，添加 --name、--age、--vip、--city 参数


# store_true vs type=bool
# TODO: 解释两者的区别


# nargs="+"
# TODO: 写一个接收多个值的参数


# if __name__ == "__main__":
# TODO: 解释作用


# dataclass → dict → JSON
# TODO: 写出 asdict + json.dumps 的完整流程



# ==================== 本周核心一句话 ====================
#
# 变量是标签，不是盒子
# 函数只做计算，异常在外层捕获
# with open 确保文件关闭
# @dataclass 自动生成 init/repr/eq
# argparse 处理命令行参数，store_true 做布尔开关
# json.dumps + asdict 实现 dataclass → JSON 输出
# if __name__ == "__main__": 保护入口不被 import 执行
