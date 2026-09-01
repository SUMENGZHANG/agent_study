"""Day 10 练习：并发调用 3 个模拟模型接口（约 30 行核心代码）。"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


@dataclass
class ModelTask:
    name: str
    delay: float        # 模拟耗时（秒）
    should_fail: bool = False  # 模拟接口报错


@dataclass
class ModelResult:
    name: str
    ok: bool
    detail: str


# TODO 1: 实现一个协程，模拟调用单个模型接口。
#   - await asyncio.sleep(task.delay)
#   - task.should_fail 为 True 时抛出 ValueError("接口故障")
#   - 否则返回 f"{task.name} 返回 ok"
async def call_model(task: ModelTask) -> str:

    raise NotImplementedError("请实现 call_model")


# TODO 2: 实现并发调用，整体超时抛 TimeoutError。
#   要求：
#   1. 用 asyncio.gather 并发执行所有任务，但单个任务的异常不能让整体崩溃
#      （提示：gather(..., return_exceptions=True)）
#   2. 用 asyncio.wait_for 给整体加超时，超时时抛出 TimeoutError
#   3. 把每个任务的结果包装成 ModelResult：
#      - 成功：ok=True，detail 是返回字符串
#      - 失败：ok=False，detail 是异常信息（str(exc)）
#   4. 返回结果顺序与 tasks 顺序一致
async def fetch_all_models(tasks: list[ModelTask], timeout: float) -> list[ModelResult]:
    asyncio.gather(tasks, return_exceptions=True)
    res = []
    try:
       results = await asyncio.wait_for(tasks, timeout)
       for task, result in zip(tasks, results):
           if isinstance(result, Exception):
               res.append(ModelResult(task.name, False, str(result)))
           else:
               res.append(ModelResult(task.name, True, result))

    except TimeoutError:
        raise TimeoutError("整体超时")

    return res


# TODO 3（选做）: 实现串行版本，用于对比耗时。
#   逐个调用 call_model，失败时同样包装成 ModelResult 而不是中断。
async def fetch_serial(tasks: list[ModelTask]) -> list[ModelResult]:
    raise NotImplementedError("请实现 fetch_serial")


async def main() -> None:
    tasks = [
        ModelTask("模型A", 0.5),
        ModelTask("模型B", 0.8),
        ModelTask("模型C", 0.6, should_fail=True),
    ]

    start = time.perf_counter()
    results = await fetch_all_models(tasks, timeout=2.0)
    concurrent_cost = time.perf_counter() - start

    start = time.perf_counter()
    serial_results = await fetch_serial(tasks)
    serial_cost = time.perf_counter() - start

    for r in results:
        print(f"  并发: {r}")
    print(f"  并发耗时 {concurrent_cost:.2f}s，串行耗时 {serial_cost:.2f}s")
    assert [r.name for r in results] == [t.name for t in tasks]
    assert [r.ok for r in results] == [True, True, False]
    assert [r.ok for r in serial_results] == [True, True, False]
    assert serial_cost > concurrent_cost  # 串行必须更慢
    print("  全部断言通过 ✔")

    # 超时场景：整体 0.3 秒，但任务都要 0.5 秒以上
    try:
        await fetch_all_models([ModelTask("慢模型", 0.5)], timeout=0.3)
    except TimeoutError:
        print("  超时场景通过 ✔")
    else:
        raise AssertionError("应当抛出 TimeoutError")


if __name__ == "__main__":
    asyncio.run(main())
