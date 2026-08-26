# Day 7 — 第一周复盘：语法回顾、盲写 CLI、Python vs Java 口述

> 日期：2026-07-27 | 预计用时：2 小时

---

## 今日目标

1. **复盘本周语法**：用一张速查表回顾 Day 1–6 所有核心知识点
2. **不看答案重写命令行程序**：从零盲写圈人条件生成器，检验真实掌握程度
3. **口述 Python 与 Java 差异**：类型系统、异常机制、并发模型三大维度

---

## 1. 本周语法速查表

### Day 1：变量、数字、字符串、IO

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| 动态类型 | 变量是标签，不是盒子 | `x = 10; x = "hello"` |
| 数字运算 | `/` 真除、`//` 整除、`**` 幂 | `10 / 3 → 3.33`, `10 // 3 → 3` |
| 布尔 Falsy | `0`, `""`, `[]`, `{}`, `None` → `False` | `bool("") → False` |
| f-string | `f"{expr:.2f}"` 格式化 | `f"总价：{price * qty:.2f}"` |
| input | 永远返回 `str`，需手动转型 | `age = int(input("年龄："))` |
| 类型转换 | `int()`, `float()`, `str()`, `bool()` | `int("42") → 42` |

### Day 2：集合、切片、推导式

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| list | 有序、可变、可重复 | `[1, 2, 3].append(4)` |
| tuple | 有序、不可变、可作 dict key | `(3, 4)`, `x, y = point` |
| dict | 键值对，键必须可哈希 | `d.get("key", default)` |
| set | 无序、不重复，集合运算 | `a & b` 交集 |
| 切片 | `[start:stop:step]` | `nums[::-1]` 反转 |
| 推导式 | 一行生成 list/dict/set | `[x**2 for x in range(10)]` |

### Day 3：控制流、函数、作用域

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| if/elif/else | 条件分支 | `if x > 0: ... elif x == 0: ... else: ...` |
| for | 遍历可迭代对象 | `for i, v in enumerate(items):` |
| while | 条件循环 | `while count < 3:` |
| 函数定义 | `def`, 参数, 返回值 | `def f(a, b=10) -> int:` |
| *args/**kwargs | 可变参数 | `def f(*args, **kwargs):` |
| 作用域 | 局部 vs 全局，`global` 关键字 | 函数内不能直接修改全局变量 |

### Day 4：模块、文件、JSON、异常

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| import | 四种导入方式 | `from module import func` |
| 包 | 目录 + `__init__.py` | `from pkg.sub import mod` |
| 文件读写 | `with open() as f:` 上下文管理 | `f.read()`, `f.write()` |
| JSON | `loads`/`dumps`/`load`/`dump` | `json.dumps(d, ensure_ascii=False, indent=2)` |
| try/except | 捕获具体异常 | `except ValueError as e:` |
| raise | 主动抛出异常 | `raise ValueError("msg")` |

### Day 5：类、dataclass、类型注解

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| class | `__init__`, `self`, `__repr__` | `class Dog:` |
| 继承 | 单继承/多继承，多态 | `class Cat(Animal):` |
| @dataclass | 自动生成 init/repr/eq | `@dataclass class Cond:` |
| field | 可变默认值 | `field(default_factory=list)` |
| 类型注解 | 运行时不强制，IDE 提示 | `name: str`, `x: int \| None` |
| Enum | 枚举类型 | `class Color(Enum):` |

### Day 6：argparse、CLI、JSON 输出

| 知识点 | 核心要点 | 示例 |
|--------|---------|------|
| argparse | 内置命令行解析 | `parser.add_argument("--age", type=int)` |
| store_true | 布尔开关 | `--vip` 出现即 True |
| nargs="+" | 接收多个值 | `--city hz sh` → `["hz", "sh"]` |
| `__main__` | 入口保护 | `if __name__ == "__main__":` |
| asdict | dataclass → dict | `asdict(request)` |
| CLI 结构 | 模型→逻辑→格式化→入口 | 四段式标准结构 |

---

## 2. 盲写挑战：从零重写命令行圈人条件生成器

**规则：不看 Day 5/6 的代码，凭记忆和理解从零编写。**

### 需求回顾

编写一个 `audience_generator.py` 命令行工具：

- `--min-age` / `--max-age`：年龄范围（int）
- `--gender`：性别，可选 `male` / `female`
- `--city`：城市，可传多个（`nargs="+"`）
- `--vip`：布尔开关
- `--logic`：条件逻辑，`AND`（默认）/ `OR`
- `-o` / `--output`：输出文件路径
- 输出 JSON，包含 `request_id`（uuid）、`conditions` 列表、`logic`

### 自检清单

写完后对照以下清单自检：

- [ ] 用了 `argparse` 而不是手动解析 `sys.argv`
- [ ] `--vip` 用 `action="store_true"` 而不是 `type=bool`
- [ ] 用了 `@dataclass` 定义 `Condition` 和 `AudienceRequest`
- [ ] 用了 `asdict()` 而不是 `__dict__` 转字典
- [ ] 用了 `json.dumps(ensure_ascii=False, indent=2)` 输出
- [ ] 有 `if __name__ == "__main__":` 入口保护
- [ ] 核心逻辑和 IO 分离（函数职责单一）
- [ ] 没有任何条件时给出友好提示

### 程序结构模板

```
1. import 区
2. @dataclass 数据模型
3. build_conditions(args) → list[Condition]   # 核心逻辑
4. create_parser() → ArgumentParser            # 参数定义
5. main()                                       # 主流程
6. if __name__ == "__main__": main()            # 入口
```

---

## 3. 口述练习：Python vs Java

### 维度一：类型系统

| 维度 | Python | Java |
|------|--------|------|
| 类型检查时机 | 运行时（动态类型） | 编译时（静态类型） |
| 变量声明 | 无需声明，赋值即创建 | 必须声明类型 |
| 类型注解 | 可选，运行时不强制 | 必须，编译器强制检查 |
| 类型转换 | `int("42")` 函数式 | `Integer.parseInt("42")` |
| 容器泛型 | `list[int]`（注解，不强制） | `List<Integer>`（编译时强制） |
| None/null | `None` 是单例对象 | `null` 是空引用 |

**口述要点：**
> Python 是动态类型，变量只是标签，同一个变量可以指向不同类型的对象。
> Java 是静态类型，编译时就能发现类型错误。Python 靠类型注解 + mypy 做静态检查作为补充。

### 维度二：异常机制

| 维度 | Python | Java |
|------|--------|------|
| 异常基类 | `BaseException` → `Exception` | `Throwable` → `Exception` |
| 检查型异常 | 无（所有异常都是 unchecked） | 有 checked exception，必须声明或捕获 |
| 捕获语法 | `try/except/else/finally` | `try/catch/finally` |
| 多异常捕获 | `except (A, B) as e:` | `catch (A | B e)` |
| 抛出异常 | `raise ValueError("msg")` | `throw new ValueError("msg")` |
| 自定义异常 | `class MyErr(Exception): pass` | `class MyErr extends Exception {}` |

**口述要点：**
> Python 没有 checked exception，所有异常都是运行时检查，代码更简洁但容易遗漏。
> Java 的 checked exception 强制开发者处理异常，更安全但代码更啰嗦。
> Python 的哲学是 EAFP（先做再说，出错再处理），Java 是 LBYL（先检查再做）。

### 维度三：并发模型

| 维度 | Python | Java |
|------|--------|------|
| 多线程 | 受 GIL 限制，CPU 密集无效 | 真正的多线程并行 |
| 多进程 | `multiprocessing` 模块 | 不支持原生多进程 |
| 协程 | `asyncio` + `async/await` | 虚拟线程（Java 21+ Loom） |
| GIL | 全局解释器锁，同一时刻只有一个线程执行 | 无 GIL |
| 适用场景 | IO 密集用协程，CPU 密集用多进程 | 多线程通用 |

**口述要点：**
> Python 有 GIL（全局解释器锁），同一时刻只有一个线程在执行 Python 字节码，
> 所以多线程对 CPU 密集任务没用。解决方案：IO 密集用 asyncio 协程，CPU 密集用多进程。
> Java 没有 GIL，多线程可以真正并行，适合 CPU 密集场景。Java 21 引入虚拟线程（Loom），
> 类似 Python 的协程但由 JVM 调度。

---

## 4. 每日作业

### 作业 1：盲写 CLI 程序（必做）

不看 Day 5/6 的代码，从零重写命令行圈人条件生成器，写到 `day07/work.py` 中。

### 作业 2：语法复盘练习（必做）

在 `day07/day07_notes.py` 中，凭记忆写出本周学过的所有核心语法示例。

### 作业 3：口述三道题（必做）

不看代码，口述以下问题（10 分钟），答案写在 `work.py` 底部注释区：

1. 从类型系统、异常机制、并发模型三个维度，对比 Python 和 Java 的核心差异
2. 本周学的 `@dataclass`、`argparse`、`json.dumps` 三者的协作流程是什么？
3. `if __name__ == "__main__":` 的作用？不加会怎样？`store_true` 和 `type=bool` 的区别？

---

## 5. 完成标准

- [ ] 盲写的 CLI 程序能正确运行 `--help` 和各种参数组合
- [ ] 能不看代码口述 10 分钟本周知识点
- [ ] 能清晰讲出 Python vs Java 在类型、异常、并发三方面的差异
- [ ] 自检清单全部通过
