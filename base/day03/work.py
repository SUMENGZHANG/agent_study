"""
作业 1：根据标签条件筛选用户（必做）

用今天学的 if、for、while、函数、参数和返回值，
实现一个“根据标签条件筛选用户”的小工具。

要求：
- 使用函数封装逻辑
- 使用 dict.get() 安全访问标签
- 使用 f-string 输出结果
- 支持多个条件同时满足（AND 关系）
- 至少支持 ==、!=、>、>=、<、<= 六种操作符
"""
from typing import Any

# TODO: 定义示例用户列表
class User:
    def __init__(self, user_id: int, name: str, tags: dict):
        self.user_id = user_id
        self.name = name
        self.tags = tags
# 每个用户包含 user_id、name 和 tags（字典）
users = []
# TODO: 实现函数：安全获取用户的某个标签值
# 函数签名参考：def get_tag(user: User, tag_name: str) -> Any
def get_tag(user: User,tag_name: str) ->Any:
    if tag_name in user.tags:
        return user.tags[tag_name]
    else:
        return None

# TODO: 实现函数：判断单个用户是否满足一个条件
# condition 格式：{"tag": "age", "op": ">=", "value": 18}
# 如果用户没有该标签，返回 False
# 支持 ==、!=、>、>=、<、<= 六种操作符
def match_condition(user: User, condition:dict) -> bool:
    tag_name = condition["tag"]
    if tag_name not in user.tags:
        return False;

    if condition["op"] == "==":
        return user.tags[tag_name] == condition["value"]
    elif condition["op"] == "!=":
        return user.tags[tag_name] != condition["value"]
    elif condition["op"] == ">":
        return user.tags[tag_name] > condition["value"]
    elif condition["op"] == ">=":
        return user.tags[tag_name] >= condition["value"]
    elif condition["op"] == "<":
        return user.tags[tag_name] < condition["value"]
    elif condition["op"] == "<=":
        return user.tags[tag_name] <= condition["value"]
    return True


# TODO: 实现函数：根据多个条件筛选用户
# 所有条件需同时满足（AND 关系）
# 返回满足条件的用户列表
def match_all(user:User,conditions:list) -> bool:
    for condition in conditions:
        if not match_condition(user, condition):
            return False
    return True



# TODO: 使用 while 循环实现一个功能：
# 不断从 conditions 列表中取出条件，直到列表为空或遇到不满足的条件
# 可以用这个思路重写上面的多条件匹配逻辑

def match_loop(user:User, conditions:list) -> bool:
    while len(conditions) > 0:
        condition = conditions.pop(0)
        if not match_condition(user, condition):
            return False
    return True


# TODO: 用 f-string 打印筛选结果
# 输出格式示例："找到 N 个用户：Alice, Bob"


"""
作业 2：函数参数与作用域小练习（必做）

1. 写一个带有默认参数的函数
2. 写一个使用 *args 的函数
3. 写一个使用 **kwargs 的函数
4. 写一个修改全局变量的函数（使用 global）
"""

# TODO: 1. 带有默认参数的函数
def default_param(a=1, b=2, c=3):
    return a + b + c


# TODO: 2. 使用 *args 的函数
def args_func(a:int,b:int,*args):
    print(a, b, args)

def args_test(a:int,b:int,c:dict):
    print(a, b, c)

# TODO: 3. 使用 **kwargs 的函数
def kwargs_func(a:int,b:int,**kwargs):
    print(a, b, kwargs)

args_func(1,3,4,5,6)

x = 0
# TODO: 4. 修改全局变量的函数
def global_func():
    global x
    x = 10


kwargs_func(1, 2, c=1,d=1)
"""
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. return 和 print 有什么区别？什么时候用 return？
2. 函数参数里的 *args 和 **kwargs 分别是什么？
3. 局部变量和全局变量有什么区别？函数里能直接修改全局变量吗？
"""
