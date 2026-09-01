"""Day 8 Demo — 包结构与 import。

运行：python demo.py
要点：脚本所在目录会自动进入 sys.path，因此能直接 import 同目录的 demo_pkg。
"""
from __future__ import annotations

import sys

# 方式 1：从 __init__.py 的统一出口导入（推荐）
from demo_pkg import Condition, build_age_condition, summarize
# 方式 2：绝对导入直达具体模块（外部也允许，但绕过统一出口）
from demo_pkg.models import Condition as DeepCondition


def main() -> None:
    print("1. 通过 __init__.py 统一出口使用包：")
    c1 = build_age_condition(18)
    c2 = Condition("city", "==", "hangzhou")
    print("  ", summarize([c1, c2], logic="AND"))

    print("2. 两种导入路径拿到的是同一个类:", DeepCondition is Condition)

    print("3. sys.path 第一项 = 脚本所在目录（import 从这里开始找）:")
    print("  ", sys.path[0])

    print("4. 当前解释器（遇到 ModuleNotFoundError 先检查这个）:")
    print("  ", sys.executable)


if __name__ == "__main__":
    main()
