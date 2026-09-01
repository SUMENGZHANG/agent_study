"""Day 10 并发 demo：用"模拟模型接口"对比串行、线程、协程。"""

from __future__ import annotations

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS = [("模型A", 0.5), ("模型B", 0.8), ("模型C", 0.6)]


# ==================== 1. 串行：总耗时 = 各任务之和 ====================

def call_model_sync(name: str, delay: float) -> str:
    time.sleep(delay)  # 模拟模型接口的网络耗时
    return f"{name} 返回 ok"


def run_serial() -> float:
    start = time.perf_counter()
    for name, delay in MODELS:
        print("  ", call_model_sync(name, delay))
    return time.perf_counter() - start


# ==================== 2. 线程：总耗时 ≈ 最慢的那个任务 ====================

def run_threads() -> float:
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(call_model_sync, name, delay) for name, delay in MODELS]
        for future in as_completed(futures):  # 谁先完成谁先返回
            print("  ", future.result())
    return time.perf_counter() - start


# ==================== 3. 协程：单线程 + 事件循环 ====================

async def call_model_async(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # await 让出执行权，别人可以先跑
    return f"{name} 返回 ok"


async def run_coroutines() -> float:
    start = time.perf_counter()
    results = await asyncio.gather(  # 结果顺序与传入顺序一致
        *(call_model_async(name, delay) for name, delay in MODELS)
    )
    for result in results:
        print("  ", result)
    return time.perf_counter() - start


# ==================== 4. 协程的超时控制 ====================

async def demo_timeout() -> None:
    try:
        await asyncio.wait_for(call_model_async("慢模型", 5.0), timeout=1.0)
    except asyncio.TimeoutError:
        print("   超时！超过 1.0 秒直接放弃，不再等")


# ==================== 5. 线程共享变量必须加锁 ====================

def demo_lock() -> None:
    counter = 0
    lock = threading.Lock()

    def add_times(n: int) -> None:
        nonlocal counter
        for _ in range(n):
            with lock:  # 不加锁时，最终结果通常小于预期
                counter += 1

    threads = [threading.Thread(target=add_times, args=(100_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"   4 个线程各加 10 万次，结果 = {counter}（预期 400000）")


if __name__ == "__main__":
    print("1. 串行调用 3 个模型接口：")
    serial = run_serial()
    print(f"   耗时 {serial:.2f}s\n")

    print("2. 线程池并发调用：")
    threaded = run_threads()
    print(f"   耗时 {threaded:.2f}s\n")

    print("3. asyncio 协程并发调用：")
    async_time = asyncio.run(run_coroutines())
    print(f"   耗时 {async_time:.2f}s\n")

    print("4. 协程超时控制：")
    asyncio.run(demo_timeout())
    print()

    print("5. 线程共享变量 + Lock：")
    demo_lock()
    print()

    print(f"结论：串行 {serial:.2f}s vs 并发 ~{min(threaded, async_time):.2f}s")
    print("I/O 等待被重叠了，这就是并发的收益。")
