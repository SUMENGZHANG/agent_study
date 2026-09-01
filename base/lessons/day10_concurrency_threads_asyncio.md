# Day 10 — Python 并发：进程、线程、协程与 async/await

> 日期：2026-07-30 | 预计用时：2 小时

---

## 1. 为什么要学并发

Agent 场景中一次请求往往要同时调多个模型接口、多个标签检索服务。如果串行调用，每个接口 2 秒，3 个就是 6 秒；并发调用只需约 2 秒。并发的本质：**在等待（I/O）的时候不要干等，去做别的事**。

## 2. 三个核心概念：进程、线程、协程

| 概念 | 是什么 | 切换成本 | 内存 | 谁调度 |
|------|--------|----------|------|--------|
| 进程 (Process) | 一个运行中的程序，有独立内存 | 高 | 大 | 操作系统 |
| 线程 (Thread) | 进程内的一条执行流，共享内存 | 中 | 中 | 操作系统 |
| 协程 (Coroutine) | 函数级的轻量执行流，共享一个线程 | 极低 | 极小 | 程序自己（事件循环） |

一句话记忆：

- **进程** = 独立的工厂（隔离最安全，通信最贵）
- **线程** = 工厂里的工人（共享工具，但会抢工具打架）
- **协程** = 一个工人同时照看多台机器（机器运转时去看别的机器）

### 2.1 GIL：Python 线程的"特殊规则"

CPython 有全局解释器锁（GIL）：**同一时刻只有一个线程执行 Python 字节码**。后果：

- **CPU 密集**（大量计算）：多线程没用，要用多进程绕过 GIL
- **I/O 密集**（等网络/文件/模型接口）：`time.sleep`、网络请求会释放 GIL，多线程有效

| 任务类型 | 推荐方案 |
|----------|----------|
| I/O 密集（调模型接口、查数据库） | 线程池 或 asyncio |
| CPU 密集（大量数值计算） | 多进程池 |

对比 Java：Java 没有 GIL，多线程可真并行计算；这是面试高频对比点。

## 3. threading：线程基础

```python
import threading
import time

def call_model(name: str, delay: float) -> None:
    time.sleep(delay)               # 模拟模型接口耗时
    print(f"{name} 返回")

t1 = threading.Thread(target=call_model, args=("模型A", 1.0))
t2 = threading.Thread(target=call_model, args=("模型B", 1.0))
t1.start(); t2.start()
t1.join();  t2.join()               # 等两个线程都结束
```

### 3.1 共享数据的坑：竞态条件

线程共享内存，同时读写一个变量会出错，必须加锁：

```python
lock = threading.Lock()
counter = 0

def add():
    global counter
    with lock:                      # 临界区：一次只进一个线程
        counter += 1
```

经验法则：**能不用共享变量就不用；必须共享就上锁**。

## 4. concurrent.futures：线程池 / 进程池

手写 Thread 管理起来麻烦，标准做法是线程池：

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# I/O 密集：ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(call_model, name, 1.0) for name in ("A", "B", "C")]
    for future in as_completed(futures):   # 谁先完成谁先返回
        future.result()                     # 取结果；任务里抛的异常在这里重新抛出

# CPU 密集：把上面换成 ProcessPoolExecutor 即可，接口完全一样
```

要点：

- `submit()` 提交任务立刻返回 `Future`（"占位凭证"）
- `future.result()` 阻塞等结果，或加 `timeout`
- `as_completed()` 按完成顺序迭代
- `with` 退出时自动等所有任务结束

## 5. asyncio：协程与事件循环

### 5.1 三个关键词

```python
import asyncio

async def call_model(name: str, delay: float) -> str:   # async def = 协程函数
    await asyncio.sleep(delay)          # await = "我要等，先让出执行权"
    return f"{name} 返回"

async def main():
    results = await asyncio.gather(     # 并发跑多个协程，一起等
        call_model("A", 1.0),
        call_model("B", 1.0),
        call_model("C", 1.0),
    )
    print(results)

asyncio.run(main())                     # 启动事件循环（程序入口只调一次）
```

- `async def` 定义的函数调用后不会执行，只返回一个协程对象
- 协程必须被 `await` 或交给事件循环才会真正执行
- `await` 只在 `async` 函数里可用
- 事件循环 = 单线程上的调度器：谁在等就切到别人

### 5.2 常用并发原语

```python
# 并发执行 + 收集全部结果（一个失败全部失败）
results = await asyncio.gather(*tasks)

# 超时控制
result = await asyncio.wait_for(call_model("A", 5.0), timeout=2.0)
# 超时抛 asyncio.TimeoutError

# 按完成顺序处理
tasks = [asyncio.create_task(call_model(n, d)) for n, d in ...]
for coro in asyncio.as_completed(tasks):
    result = await coro
```

### 5.3 协程的致命陷阱：阻塞调用

事件循环只有一个线程。在协程里调用阻塞函数（`time.sleep`、同步 `requests`），整个循环卡死，所有并发任务陪葬：

```python
# ❌ 在 async 函数里
time.sleep(1)              # 卡死整个事件循环

# ✅ 正确做法
await asyncio.sleep(1)     # 让出执行权，别人可以继续跑
```

这就是为什么生产里要用 `httpx`/`aiohttp` 等异步 HTTP 客户端。

## 6. 怎么选？

```
任务要并发吗？
├── 等 I/O（网络、模型接口、文件）
│   ├── 简单脚本/已有同步代码 → ThreadPoolExecutor
│   └── 新项目/大量并发（几百上千） → asyncio
└── 算得多（CPU 密集） → ProcessPoolExecutor
```

Agent 技术栈里的位置：FastAPI 路由支持 `async def`、LangGraph 节点有异步版本、模型 SDK 大多提供 `async` 接口——所以**第二周之后你写的代码基本都会走 asyncio 这条路**。

## 7. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| 真并行计算 | 多进程绕 GIL | 多线程直接并行 |
| 线程池 | `ThreadPoolExecutor` | `ExecutorService` |
| 协程/异步 | `async/await` + 事件循环 | `CompletableFuture` / 虚拟线程 |
| 等待结果 | `future.result(timeout=...)` | `future.get(timeout, ...)` |
| 并发原语锁 | `threading.Lock` | `synchronized` / `ReentrantLock` |
| 休眠模拟 | `time.sleep` / `await asyncio.sleep` | `Thread.sleep` |

## 8. 常见错误清单

```python
# ❌ 忘了 await：只得到协程对象，函数根本没执行
call_model("A", 1)            # RuntimeWarning: coroutine was never awaited
await call_model("A", 1)      # ✅

# ❌ gather 顺序传参搞错：结果顺序 = 任务顺序，与完成顺序无关

# ❌ 线程里改共享变量不加锁 → 结果偶发错误，最难查的 bug

# ❌ 在 async 里调阻塞库 → 并发退化成串行，性能没提升还更难调试
```

## 9. 今日练习（见 `base/day10/work.py`）

实现 `fetch_all_models(models, timeout)`：用 asyncio 并发调用 3 个模拟模型接口，要求：

1. 每个接口用 `await asyncio.sleep(delay)` 模拟
2. 整体有超时，超时抛 `TimeoutError`
3. 某个接口返回错误时，结果里明确标记失败原因，而不是让程序崩溃
4. 对比串行耗时与并发耗时，打印出来

完成标准：能说清"为什么这里用协程而不是线程"以及"阻塞调用会怎样"。
