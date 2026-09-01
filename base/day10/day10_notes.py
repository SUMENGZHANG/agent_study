"""
Day 10 并发速查笔记

对应课程：lessons/day10_concurrency_threads_asyncio.md
先不看课程，凭理解填 TODO；填完再对照查漏。
"""

# ==================== 1. 概念：进程 / 线程 / 协程 ====================

# TODO: 用自己的话写出三者的区别（切换成本、内存、谁调度）
# 进程：
# 线程：
# 协程：

# TODO: GIL 是什么？它对 CPU 密集和 I/O 密集任务分别意味着什么？

# TODO: 选型口诀——I/O 密集用什么？CPU 密集用什么？


# ==================== 2. threading ====================

# TODO: 写一个最小的线程示例：起一个线程执行函数，主线程等待它结束
# 提示：threading.Thread(target=..., args=...) / start() / join()


# TODO: 两个线程同时给同一个变量 +1，不加锁会发生什么？
# TODO: 用 threading.Lock 修复上面的问题（with lock: ...）


# ==================== 3. concurrent.futures ====================

# TODO: 用 ThreadPoolExecutor 并发执行 3 个任务，收集结果
# 提示：pool.submit() 返回 Future；future.result() 取结果

# TODO: as_completed 和直接遍历 futures 的区别是什么？

# TODO: 把 ThreadPoolExecutor 换成 ProcessPoolExecutor 适用于什么场景？


# ==================== 4. asyncio ====================

# TODO: async def 定义的函数直接调用会发生什么？怎样才会真正执行？

# TODO: 写一个协程函数，用 await asyncio.sleep(1) 模拟耗时操作

# TODO: 用 asyncio.gather 并发跑 3 个协程并收集结果

# TODO: asyncio.run() 的作用是什么？一个程序里能调用几次？

# TODO: 给一个协程加超时控制，超时抛异常（提示：asyncio.wait_for）

# TODO: 在 async 函数里调用 time.sleep 会有什么问题？正确写法是什么？


# ==================== 5. 今日核心一句话 ====================
#
# 并发 = 等待时不闲着
# GIL 让多线程只适合 I/O 密集，CPU 密集要多进程
# 协程由事件循环调度，阻塞调用会卡死整个循环
# gather 并发收集，wait_for 控制超时
