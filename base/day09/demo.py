"""Day 9 Demo — logging 基本用法 + 用 Mock 替换"模型接口"。

运行：python demo.py
"""
from __future__ import annotations

import logging
from unittest.mock import MagicMock, patch

logger = logging.getLogger("day09.demo")


def call_model(prompt: str) -> str:
    """真实代码里会调用模型接口；demo 中让它故意不可用。"""
    raise RuntimeError("演示环境不能真的调用模型接口")


def generate_audience(prompt: str) -> str:
    """依赖 call_model 的业务逻辑——这就是要用 Mock 替换的边界。"""
    answer = call_model(prompt)
    logger.info("模型返回 %d 个字符", len(answer))
    return f"人群包: {answer}"


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.debug("debug 低于 INFO 级别，默认不会输出")
    logger.info("开始演示")

    fake_model = MagicMock(return_value='{"age": ">=18"}')
    # __main__ = 直接运行时的本文件；patch 目标是"名字被使用的地方"
    with patch("__main__.call_model", fake_model):
        result = generate_audience("圈 18 岁以上的人")

    print("业务结果:", result)
    fake_model.assert_called_once_with("圈 18 岁以上的人")
    print(f"Mock 校验通过：call_model 被调用 {fake_model.call_count} 次，参数符合预期")


if __name__ == "__main__":
    main()
