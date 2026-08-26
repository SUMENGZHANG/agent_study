"""
作业 1：命令行圈人条件生成器（必做）

编写 audience_generator.py 命令行工具，支持以下参数：

参数：
- --min-age / --max-age：年龄范围（int）
- --gender：性别，可选 male / female，非必填
- --city：城市，字符串，可传多个（nargs="+"）
- --vip：是否 VIP，布尔开关
- --logic：条件间逻辑，AND（默认）/ OR
- -o / --output：输出文件路径，不指定则打印到终端

输出格式：标准 JSON，包含 request_id（用 uuid 生成）、conditions 列表和 logic。

示例调用：
    python audience_generator.py --min-age 18 --max-age 35 --city hangzhou shanghai --vip --logic AND
"""
import argparse
import json
import uuid
from dataclasses import dataclass, asdict
from typing import Any, List, Optional
from pathlib import Path


# ========== 1. 数据模型 ==========
# @dataclass 自动生成 __init__、__repr__、__eq__，只需要声明字段和类型注解
@dataclass
class Condition:
    """圈人条件"""
    field_name: str
    operator: str
    value: Any


@dataclass
class AudienceRequest:
    """圈人请求"""
    request_id: str
    conditions: List[Condition]
    logic: str = "AND"


# ========== 2. 标签解析（作业 2） ==========
# 注意：labels.json 的 key 与 dataclass 字段名不一致，需要做映射
# JSON: "field" → dataclass: field_name
# JSON: "type"  → dataclass: label_type
# 所以不能直接复用 day05 的 parse_label/parse_condition，要自己写映射

def parse_condition(data: dict) -> Condition:
    """将 JSON dict 转为 Condition，处理 field → field_name 映射"""
    return Condition(
        field_name=data.get("field", ""),   # JSON 里是 "field"
        operator=data.get("op", ""),
        value=data.get("value"),
    )


def parse_label_conditions(data: dict) -> list[Condition]:
    """从 label JSON 中提取所有 Condition"""
    return [parse_condition(c) for c in data.get("conditions", [])]


# ========== 3. 核心业务逻辑 ==========
# 拆成两个函数：一个处理命令行参数，一个处理 label 文件

def build_cli_conditions(args: argparse.Namespace) -> list[Condition]:
    """根据命令行参数构建圈人条件列表"""
    conditions: list[Condition] = []

    if args.min_age is not None:
        conditions.append(Condition("age", ">=", args.min_age))
    if args.max_age is not None:
        conditions.append(Condition("age", "<=", args.max_age))
    if args.gender is not None:
        conditions.append(Condition("gender", "==", args.gender))
    # nargs="+" 时，args.city 是 list 或 None
    if args.city:
        conditions.append(Condition("city", "in", args.city))
    # store_true 不传时默认 False，所以用 if args.vip 即可
    if args.vip:
        conditions.append(Condition("vip", "==", True))

    return conditions


def build_label_conditions(label_file: str) -> list[Condition]:
    """从 label JSON 文件中读取并合并条件

    为什么不能直接复用 day05 的 parse_label / parse_condition？
    因为 labels.json 里的 key 和 day05 dataclass 的字段名不一致：
      - JSON: "field"       → dataclass: field_name
      - JSON: "type"        → dataclass: label_type
    day05 的 parse_condition 读的是 data["field_name"]，但 JSON 里根本没有这个 key，
    会直接报 KeyError。所以这里要自己写映射。
    """
    conditions: list[Condition] = []
    with open(label_file, "r", encoding="utf-8") as f:
        labels = json.load(f)
        for label in labels:
            # 用 extend 把列表里的元素逐个添加，而不是 append 整个列表
            conditions.extend(parse_label_conditions(label))
    return conditions


# ========== 4. 参数解析 ==========
def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(description="圈人条件生成器")

    parser.add_argument("--min-age", type=int, default=None, help="最小年龄")
    parser.add_argument("--max-age", type=int, default=None, help="最大年龄")
    parser.add_argument("--gender", choices=["male", "female"], default=None, help="性别")
    # nargs="+" 允许一次传多个值：--city hangzhou shanghai
    parser.add_argument("--city", nargs="+", type=str, default=None, help="城市（可传多个）")
    # store_true: 不传 → False，传了 → True
    parser.add_argument("--vip", action="store_true", help="是否 VIP")
    parser.add_argument("--logic", choices=["AND", "OR"], default="AND", help="条件间逻辑（默认 AND）")
    # -o / --output：同一个参数两种写法，短名和长名
    parser.add_argument("-o", "--output", type=str, default=None, help="输出 JSON 文件路径")

    return parser


# ========== 5. 主函数 ==========
def main():
    parser = create_parser()
    # 作业 2 的 --label-file 单独加，不混在作业 1 的 parser 里
    parser.add_argument("--label-file", type=str, default=None, help="标签 JSON 文件路径（作业2）")
    args = parser.parse_args()

    # 分别构建：命令行条件 + 文件条件，然后合并
    conditions = build_cli_conditions(args)
    if args.label_file:
        conditions += build_label_conditions(args.label_file)

    if not conditions:
        print("⚠ 未指定任何条件，请使用 --help 查看帮助")
        return

    request = AudienceRequest(
        request_id=str(uuid.uuid4()),
        conditions=conditions,
        logic=args.logic,
    )

    # asdict 递归地把 dataclass 转为 dict，比 __dict__ 更可靠
    output = json.dumps(asdict(request), indent=2, ensure_ascii=False)

    if args.output:
        path = Path(args.output)
        with open(path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已保存到: {path.resolve()}")
    else:
        print(output)


if __name__ == "__main__":
    main()




"""
作业 2：从 JSON 文件读取并合并条件（选做）

支持 --label-file 参数读取 Day 4 的 labels.json，
将文件中的标签条件与命令行参数合并输出。

提示：
1. parser.add_argument("--label-file", type=str, help="标签 JSON 文件路径")
2. 读取并解析 labels.json（复用 Day 4/5 的 parse_label 逻辑）
3. 将文件中的条件与命令行参数生成的条件合并
4. 注意 JSON key 映射：field → field_name, type → label_type
"""
# TODO: 在 audience_generator.py 中添加 --label-file 参数支持




"""
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. if __name__ == "__main__": 的作用是什么？不加会怎样？
   答：Python 执行一个 .py 文件时，会内置设置 __name__ = "__main__"；
       如果这个文件被别的模块 import，__name__ 就是模块名（如 "day06.work"）。
       加上这个判断后，main() 只在「直接运行」时执行，被 import 时不会自动跑。
       不加的话，别人 import 你的模块就会自动执行 main()，产生意想不到的副作用。

2. argparse 的 action="store_true" 和 type=bool 有什么区别？
   答：store_true 是一个「开关」——不传参数时为 False，传了 --vip 就变 True，
       不需要在命令行写 --vip True。
       type=bool 则要求用户在命令行传一个值（如 --vip True），而且 bool("False")
       的结果是 True（非空字符串都是 True），非常容易踩坑。
       所以对于布尔开关，永远用 action="store_true"。

3. Python 的 json.dumps() 和 Java 的 ObjectMapper 在使用上有什么不同？
   答：Python 的 json.dumps() 直接接受 dict / list / 基本类型，遇到自定义对象需要
       手动提供 default 函数（或先用 asdict 转 dict）。
       Java 的 ObjectMapper 可以通过反射自动序列化 POJO 的所有字段，还支持注解
       （如 @JsonProperty、@JsonIgnore）精细控制序列化行为，开箱即用更强。
       本质区别：Python 是动态类型，没有编译期反射信息可用，所以需要手动转换。
"""
