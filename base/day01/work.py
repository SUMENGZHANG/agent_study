'''
作业 1：温度转换器（必做）
编写一个程序，要求用户输入摄氏度，输出对应的华氏度和开尔文温度。

公式：

华氏度 = 摄氏度 × 9/5 + 32
开尔文 = 摄氏度 + 273.15
要求：

使用 input() 接收输入
使用 f-string 格式化输出，保留 1 位小数
处理非法输入（用 try/except）

'''

def temperature_converter_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def temperature_converter_to_kelvin(celsius: float) -> float:
    return celsius + 273.15


celsius_input = input("请输入摄氏度：")
try:
    celsius = float(celsius_input)
    fahrenheit = temperature_converter_to_fahrenheit(celsius)
    kelvin = temperature_converter_to_kelvin(celsius)
    print(f"{celsius:.1f} 摄氏度 = {fahrenheit:.1f} 华氏度")
    print(f"{celsius:.1f} 摄氏度 = {kelvin:.1f} 开尔文")
except ValueError:
    print("输入有误，请输入一个有效的数字！")





'''

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
'''


from datetime import datetime

name = input("输入你的名字: ")
age = int(input("输入你的年龄: "))
height = float(input("输入你的身高(米): "))
job = input("输入你的职业: ")
birth_year = datetime.now().year - age

print(f"{'=' * 10} 个人名片 {'=' * 10}")
print(f"姓名：{name}")
print(f"年龄：{age} 岁（约 {birth_year} 年出生）")
print(f"身高：{height:.2f} 米")
print(f"职业：{job}")
print(f"{'=' * 30}")
