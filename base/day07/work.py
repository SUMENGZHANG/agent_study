"""
Day 7 作业 — 第一周复盘练习

作业 1：盲写 CLI 程序（必做）
    不看 Day 5/6 的代码，凭记忆从零重写命令行圈人条件生成器。
    写完后对照 demo.py 自检。

作业 2：语法复盘练习（必做）
    在 day07_notes.py 中凭记忆写出本周核心语法示例。

作业 3：口述三道题（必做）
    不看代码，口述以下问题（10 分钟），答案写在文件底部注释区。
"""


# ========== 作业 1：盲写命令行圈人条件生成器 ==========
#
# 要求：
# 1. 用 @dataclass 定义 Condition 和 AudienceRequest
# 2. 用 argparse 解析命令行参数
# 3. 支持 --min-age, --max-age, --gender, --city, --vip, --logic, -o
# 4. 输出 JSON，包含 request_id, conditions, logic
# 5. 核心逻辑和 IO 分离
# 6. 有 if __name__ == "__main__": 入口保护
#
# TODO: 在下方开始你的盲写
#

import argparse
import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path


# TODO: 定义 Condition dataclass


# TODO: 定义 AudienceRequest dataclass


# TODO: 实现 build_conditions(args) -> list[Condition]


# TODO: 实现 create_parser() -> argparse.ArgumentParser


# TODO: 实现 main()


# TODO: 入口


# ========== 作业 2：见 day07_notes.py ==========


# ========== 作业 3：口述题（答案写在下方注释区） ==========

"""
口述题 1：从类型系统、异常机制、并发模型三个维度，对比 Python 和 Java 的核心差异

答：
TODO: 凭记忆口述，写在下方



口述题 2：@dataclass、argparse、json.dumps 三者的协作流程是什么？

答：
TODO: 凭记忆口述，写在下方



口述题 3：
  a) if __name__ == "__main__": 的作用？不加会怎样？
  b) store_true 和 type=bool 的区别？

答：
TODO: 凭记忆口述，写在下方
"""
