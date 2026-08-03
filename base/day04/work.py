"""
作业 1：标签 JSON 读取器（必做）

项目目录 base/day04/ 下有 labels.json 文件，包含多个营销标签定义。

要求：
1. 编写函数 load_labels(filepath) 读取并解析 JSON 文件
2. 处理文件不存在的情况（FileNotFoundError）
3. 处理 JSON 格式错误的情况（json.JSONDecodeError）
4. 编写函数 validate_label(label) 校验每个标签是否包含必需字段：name、type、conditions
5. 缺失字段时用 dict.get() 提供默认值，并打印警告
6. 编写函数 print_labels(labels) 格式化打印所有标签
"""
import json
from pathlib import Path


# TODO: 实现 load_labels(filepath) 函数
def load_labels(filepath: str) -> list:
    try:
        with open("labels.json", "r", encoding="utf-8") as f:
            labels = json.load(f)
            return labels
    except FileNotFoundError:
        print(f"文件 {filepath} 未找到")
        return None;
    except json.JSONDecodeError:
        print(f"文件 {filepath} JSON 解码错误")
        return None;



# TODO: 实现 validate_label(label) 函数
def validate_label(label: dict) -> bool:
    name = label.get("name", "未知名称")
    label_type = label.get("type", "未知类型")
    conditions = label.get("conditions", [])
    if not conditions:
        print(f"警告：标签 {name} 缺失 conditions 字段")
    return True

# TODO: 实现 print_labels(labels) 函数

def print_labels(labels: list):
    for label in labels:
        print(label)


# TODO: 主流程 — 加载、校验、打印


"""
作业 2：模块与包练习（必做）

1. 在 day04/ 下创建 utils.py，包含 safe_get(data, key, default) 函数
2. 在这里 from day04.utils import safe_get 使用它
3. 用这个函数安全地从标签字典中获取嵌套字段
"""

# TODO: 创建 utils.py 并在这里导入使用
from day04.utils import safe_get
safe_get({"a": {"b": 1}}, "a")


from my_package import utils
utils.safe_get({"a": {"b": 1}}, "a")



"""
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：
1. import module 和 from module import func 有什么区别？
2. 为什么推荐用 with open() 而不是直接 open()？
3. Python 和 Java 的异常体系有什么关键区别？（提示：checked vs unchecked）
"""



