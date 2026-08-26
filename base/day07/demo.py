"""
Day 7 Demo — 盲写挑战：从零重写命令行圈人条件生成器

这是复盘日提供的「参考答案骨架」，包含完整的结构提示但留空核心实现。
建议先不看本文件，自己在 work.py 中盲写，写完后再对照。

用法：
    python demo.py --help
    python demo.py --min-age 18 --max-age 35 --city hangzhou shanghai --vip
    python demo.py --gender female --logic OR -o output.json
"""
from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path


# ========== 1. 数据模型 ==========
@dataclass
class Condition:
    """单个圈人条件"""
    field_name: str
    op: str
    value: int | float | str | bool

    def describe(self) -> str:
        return f"{self.field_name} {self.op} {self.value}"


@dataclass
class AudienceRequest:
    """圈人请求"""
    request_id: str
    conditions: list[Condition] = field(default_factory=list)
    logic: str = "AND"

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "logic": self.logic,
            "conditions": [asdict(c) for c in self.conditions],
            "summary": self.summary(),
        }

    def summary(self) -> str:
        descs = [c.describe() for c in self.conditions]
        connector = " AND " if self.logic == "AND" else " OR "
        return connector.join(descs)


# ========== 2. 核心业务逻辑 ==========
def build_conditions(args: argparse.Namespace) -> list[Condition]:
    """根据命令行参数构建圈人条件列表（纯逻辑，无 IO）"""
    conditions: list[Condition] = []

    if args.min_age is not None:
        conditions.append(Condition("age", ">=", args.min_age))
    if args.max_age is not None:
        conditions.append(Condition("age", "<=", args.max_age))
    if args.gender is not None:
        conditions.append(Condition("gender", "==", args.gender))
    if args.city:
        conditions.append(Condition("city", "in", args.city))
    if args.vip:
        conditions.append(Condition("vip", "==", True))

    return conditions


def build_request(args: argparse.Namespace) -> AudienceRequest:
    """构建完整的圈人请求"""
    conditions = build_conditions(args)
    return AudienceRequest(
        request_id=str(uuid.uuid4())[:8],
        conditions=conditions,
        logic=args.logic,
    )


# ========== 3. 输出格式化 ==========
def format_output(request: AudienceRequest, indent: int = 2) -> str:
    """将圈人请求格式化为 JSON 字符串"""
    return json.dumps(request.to_dict(), ensure_ascii=False, indent=indent)


def save_to_file(content: str, filepath: str) -> None:
    """保存内容到文件"""
    path = Path(filepath)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已保存到: {path.resolve()}")


# ========== 4. 参数解析 ==========
def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="圈人条件生成器 — 复盘日盲写版",
        epilog="示例: python demo.py --min-age 18 --max-age 35 --city hangzhou --vip",
    )

    parser.add_argument("--min-age", type=int, default=None, help="最小年龄（含）")
    parser.add_argument("--max-age", type=int, default=None, help="最大年龄（含）")
    parser.add_argument("--gender", choices=["male", "female"], default=None, help="性别")
    parser.add_argument("--city", nargs="+", type=str, default=None, help="城市（可传多个）")
    parser.add_argument("--vip", action="store_true", help="是否只圈 VIP 用户")
    parser.add_argument("--logic", choices=["AND", "OR"], default="AND", help="条件间逻辑（默认 AND）")
    parser.add_argument("-o", "--output", type=str, default=None, help="输出 JSON 文件路径")

    return parser


# ========== 5. 主函数 ==========
def main():
    parser = create_parser()
    args = parser.parse_args()

    # 构建请求
    request = build_request(args)

    if not request.conditions:
        print("⚠ 未指定任何条件，请使用 --min-age / --gender / --city / --vip 等参数")
        print("  运行 python demo.py --help 查看帮助")
        return

    # 打印摘要
    print(f"圈人请求 [{request.request_id}]")
    print(f"逻辑: {request.logic}")
    print(f"条件数: {len(request.conditions)}")
    for c in request.conditions:
        print(f"  - {c.describe()}")
    print()

    # 输出 JSON
    output = format_output(request)
    if args.output:
        save_to_file(output, args.output)
    else:
        print("JSON 输出:")
        print(output)


if __name__ == "__main__":
    main()
