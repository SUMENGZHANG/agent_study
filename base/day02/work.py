'''
作业 1：标签管理器（必做）

用 dict 和 list 实现一个简易营销标签管理系统：

1. 定义至少 3 个标签（用 dict 表示，包含 name、type、description）
2. 将所有标签存入一个 list
3. 写一个函数，按 type 筛选标签并打印
4. 写一个函数，查找某个 name 的标签并返回
5. 用推导式生成一个只包含标签 name 的列表

要求：
- 使用 dict.get() 安全访问字段
- 使用 f-string 格式化输出
- 使用 for...in 遍历和 enumerate
'''
from typing import Any

# TODO: 定义标签列表
user = {
    "name":"sumeng",
    "age":18,
    "height":1.75
}


# TODO: 写按 type 筛选的函数
labels = []
for i in user.keys():
    value = user[i]
    if isinstance(value, str):
        type_name = "string"
    elif isinstance(value, int):
        type_name = "int"
    elif isinstance(value, float):
        type_name = "float"
    else:
        type_name = "unknown"
    labels.append({"name": i, "type": type_name, "description": str(value)})


def filter_by_type(label_type: str) -> None:
    print(f"类型为 '{label_type}' 的标签：")
    for index, label in enumerate(labels, start=1):
        if label.get("type") == label_type:
            name = label.get("name", "未知")
            description = label.get("description", "无描述")
            print(f"{index}. {name}: {description}")


# TODO: 写按 name 查找的函数

def read_by_name(name: str) -> Any | None:
    for label in labels:
        if label.get("name") == name:
            return label
    return None


# TODO: 用推导式生成 name 列表

names = [label.get("name") for label in labels]

'''
作业 2：数据分析小练习（必做）

给定以下数据：
'''

scores = [85, 92, 78, 95, 88, 76, 90, 83, 97, 72]

# TODO: 1. 用切片取出前 3 个和后 3 个成绩
first_three_scores = scores[:3]
print(first_three_scores)
first_three_scores = scores[-3:]
print(first_three_scores)


# TODO: 2. 用推导式筛选出 90 分以上的成绩

scores_above_90 = [score for score in scores if score > 90]

scores_above_90_for_me = [score for score in scores if score> 90]

# TODO: 3. 计算平均分（用 sum() 和 len()）
average_score = sum(scores) / len(scores)

# TODO: 4. 用推导式生成 dict：{索引: 成绩}，只包含及格（>=60）的成绩
scores_dict = {index:score for index, score in enumerate(scores) if score >= 60}
scores_dict = {index: score for index, score in enumerate(scores) if score >= 60}
# TODO: 5. 将成绩转为 set 去重，再转回 list 排序
scores_set = set(scores)

scores_list = list(scores_set)
scores_list.sort()

'''
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. list 和 tuple 有什么区别？什么时候该用哪个？
list是列表，tuple是元祖吧，元祖不可变
2. dict 的 key 为什么必须是不可变类型？（提示：哈希）
key是用来作hash的
3. Python 的 set 和 Java 的 HashSet 在底层实现上有什么共同点？
底层都是用hashTable实现的
'''
