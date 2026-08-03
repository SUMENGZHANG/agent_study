# Day 03：控制流、函数与作用域

## 今日目标

- 掌握 `if / elif / else` 分支判断
- 掌握 `for` 循环、`while` 循环和 `range()`
- 掌握函数定义、参数、返回值
- 理解局部变量与全局变量的作用域
- 实现“根据标签条件筛选用户”的函数

---

## 1. 分支判断：if / elif / else

```python
age = 25

if age < 13:
    print("儿童")
elif age < 20:
    print("青少年")
else:
    print("成年人")
```

注意：
- `elif` 可以写多个
- `else` 可选
- 条件表达式最终会被转成布尔值

---

## 2. 循环

### for 循环

用于遍历可迭代对象：

```python
for user in users:
    print(user["name"])
```

需要索引时用 `enumerate`：

```python
for index, user in enumerate(users, start=1):
    print(f"{index}. {user['name']}")
```

生成数字序列用 `range`：

```python
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)
```

### while 循环

在条件为真时反复执行：

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

注意避免死循环。

---

## 3. 函数

### 定义函数

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

- `def` 开头
- 函数名后加括号
- 参数可以有类型注解
- `return` 返回值

### 参数类型

| 参数形式 | 示例 | 说明 |
|---|---|---|
| 位置参数 | `def f(a, b)` | 按顺序传 |
| 默认参数 | `def f(a, b=10)` | 不传就用默认值 |
| 可变位置参数 | `def f(*args)` | 接收多余位置参数，元组 |
| 可变关键字参数 | `def f(**kwargs)` | 接收多余关键字参数，字典 |

```python
def demo(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)

demo(1, 3, 4, 5, x=6, y=7)
# 输出：1 3 (4, 5) {'x': 6, 'y': 7}
```

---

## 4. 作用域

### 局部变量

在函数内部定义，只在函数内部有效：

```python
def func():
    x = 10

func()
print(x)  # 报错：NameError
```

### 全局变量

在函数外部定义，模块内可见。函数内可以读取，但不能直接修改：

```python
counter = 0

def increment():
    global counter
    counter += 1
```

需要修改时，用 `global` 声明。

---

## 5. 今日作业思路

### 根据标签条件筛选用户

1. 定义用户列表，每个用户包含 `user_id`、`name`、`tags`
2. 写 `get_tag(user, tag_name)` 安全读取标签
3. 写 `match_condition(user, condition)` 判断单个条件
4. 写 `filter_users(users, conditions)` 组合多个条件
5. 用 f-string 输出结果

条件格式示例：

```python
{"tag": "age", "op": ">=", "value": 18}
{"tag": "city", "op": "==", "value": "hangzhou"}
```

---

## 6. 常见错误

- 用 `=` 而不是 `==` 做比较
- `while` 循环忘记更新条件变量，导致死循环
- 函数里想改全局变量但忘记写 `global`
- 默认参数使用可变对象（如 `def f(x=[])`），会导致意外共享

---

## 7. 口述要点

能够不看代码说出：

1. `if / elif / else` 的执行顺序
2. `for` 和 `while` 的区别
3. `return` 和 `print` 的区别
4. `*args` 和 `**kwargs` 的区别
5. 局部变量和全局变量的区别
