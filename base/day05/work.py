"""
作业 1：数据模型定义（必做）

用 dataclass 定义以下三个数据模型：

1. Condition — 圈人条件
   - field_name: str — 字段名（如 "age"）
   - op: str — 操作符（如 ">="）
   - value: int | float | str | bool — 目标值

2. Label — 营销标签
   - name: str — 英文标识
   - display_name: str — 中文显示名
   - label_type: str — 标签类型
   - conditions: list[Condition] — 条件列表
   - 实现方法 validate() 校验 name 和 conditions 不为空

3. AudienceRequest — 圈人请求
   - request_id: str — 请求 ID
   - labels: list[Label] — 使用的标签
   - logic: str — 标签间逻辑（"AND" / "OR"），默认 "AND"
   - 实现方法 summary() 打印请求摘要
"""
from __future__ import annotations

from dataclasses import dataclass, field


# TODO: 实现 Condition dataclass

@dataclass
class Condition:
    field_name:str
    op:str
    value:int|float|str|bool



# TODO: 实现 Label dataclass（含 validate 方法）
@dataclass
class Label:
    name:str
    display_name:str
    label_type:str
    conditions:list[Condition]=field(default_factory=list)

    def validate(self) -> bool:
        return self.name is not None and self.conditions is not None

# TODO: 实现 AudienceRequest dataclass（含 summary 方法）
@dataclass
class AudienceRequest:
    request_id:str
    labels:list[Label]
    logic:str = "AND"

    def summary(self) -> None:
        print(f"{self.request_id}: {self.labels}:{self.logic}")


# TODO: 创建几个 Condition 和 Label 对象，组装一个 AudienceRequest 并打印 summary
c1 = Condition("c1",">",100)
c2 = Condition("c2","<=",200)

l1 = Label("l1","标签1","type1",[c1,c2])

l2 = Label("l2","标签2","type2",[c1])


request = AudienceRequest("REQ-001",[l1,l2],"AND")



"""
作业 2：从 JSON 构建对象（必做）

读取 Day 4 的 labels.json 文件，将每个 JSON 字典转为 Label 对象，
并用 AudienceRequest 组装一个完整的圈人请求。

提示：
1. 用 json.load() 读取文件
2. 编写 parse_condition(data) 和 parse_label(data) 函数
3. 用列表推导式批量转换
4. 过滤出 validate() 为 True 的标签
5. 组装 AudienceRequest 并调用 summary()
"""
import json
from pathlib import Path


# TODO: 实现 parse_condition(data) 函数


def parse_condition(data):

    return Condition(data["field_name"], data["op"], data["value"])


# TODO: 实现 parse_label(data) 函数
def parse_label(data):
    return Label(data["name"], data["display_name"], data["label_type"], [parse_condition(c) for c in data["conditions"]])

# TODO: 读取 labels.json，转为 Label 对象，组装 AudienceRequest

labels: list[Label] = []
with open("./day04/labels.json") as f:
    raw_labels = json.load(f)
    for raw_label in raw_labels:
        cur_label = parse_label(raw_label)
        if cur_label.validate():
            parsed_conditions = [parse_condition(c) for c in cur_label.conditions]
            cur_label.conditions = parsed_conditions
            labels.append(cur_label)
request  = AudienceRequest("REQ-001",labels,"AND")


"""
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. @dataclass 和普通 class 什么时候该用哪个？
@dataclass作为数据对象的时候，方便可以不写 _repr_ 和 _eq_这些
2. Python 的 self 和 Java 的 this 有什么区别？

3. Python 的类型注解和 Java 的类型系统有什么本质不同？（提示：运行时 vs 编译时）

"""
