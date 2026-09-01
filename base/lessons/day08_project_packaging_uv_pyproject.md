# Day 8 — Python 工程化：虚拟环境、uv、pyproject.toml 与包结构

> 日期：2026-07-28 | 预计用时：2 小时

---

## 1. 为什么需要虚拟环境

一台机器上会装很多项目的依赖，A 项目要 `requests 2.0`，B 项目要 `requests 3.0`，装在全局就打架。**虚拟环境 = 每个项目独立的依赖目录**。

本项目就有自己的虚拟环境：`.venv/`，解释器在 `.venv/bin/python`。

```bash
# 查看当前用的是哪个 Python
which python

# 传统方式：python 自带 venv
python -m venv .venv
source .venv/bin/activate        # macOS/Linux 激活
deactivate                       # 退出

# 现代方式：uv（本项目使用）
uv venv                          # 创建 .venv
uv add requests                  # 加依赖（自动装 + 写入 pyproject + 锁版本）
uv add --dev pytest              # 加开发依赖
uv run python demo.py            # 在项目环境中运行，无需手动激活
```

| 工具 | 定位 | 速度 | 管理锁文件 |
|------|------|------|-----------|
| pip + venv | 官方基础工具 | 慢 | 无 |
| uv | Rust 写的新一代工具 | 快 10–100 倍 | `uv.lock` |

> `pyproject.toml` 声明"要什么"，`uv.lock` 锁定"具体哪个版本"，提交到 Git 的是这两个文件，不是 `.venv`。

## 2. pyproject.toml：项目的"身份证"

本项目的真实配置（`/pyproject.toml`）：

```toml
[project]
name = "agent-study"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "langchain-core==0.3.83",
    "langgraph==0.6.11",
    "pydantic==2.13.4",
]

[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```

要点：

- `dependencies`：运行必需（业务库）
- `[dependency-groups] dev`：只在开发时用（测试、格式化），部署不带
- `requires-python`：限定解释器版本
- 可加 `[project.scripts]` 定义命令行入口：`my-cli = "mypkg.main:main"`

## 3. 包结构：怎样组织多个文件

```text
my_project/
├── pyproject.toml
├── src/                    # src 布局（推荐，防止误 import）
│   └── mypkg/
│       ├── __init__.py     # 有它，目录才是"包"
│       ├── models.py
│       └── services.py
└── tests/
    └── test_services.py
```

- `__init__.py` 标记目录是包，可以在里面做"统一出口"（见 `base/day08/demo_pkg/__init__.py`）
- **模块内引用**用相对导入：`from .models import Condition`
- **跨包引用**用绝对导入：`from mypkg.models import Condition`
- 相对导入只能在包内部用，`from ..` 最多到父包

## 4. import 的本质：sys.path 查找

`import foo` 时，Python 按 `sys.path` 列表逐目录找 `foo.py` 或 `foo/` 包：

1. 脚本所在目录（`python demo.py` 时 demo.py 的目录）
2. `PYTHONPATH` 环境变量
3. 环境自带的 site-packages（装过的第三方库）

三类常见报错及原因：

| 报错 | 原因 |
|------|------|
| `ModuleNotFoundError: No module named 'x'` | sys.path 里没有，或没装依赖、没激活环境 |
| `ImportError: attempted relative import with no known parent package` | 用 `python pkg/mod.py` 直接跑包内文件，包身份丢失 |
| 改了代码不生效 | 跑的不是当前环境的解释器（`which python` 检查） |

**口诀：入口脚本放包外，包内全部相对导入，外部一律绝对导入。**

## 5. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| 依赖声明 | `pyproject.toml` | `pom.xml` / `build.gradle` |
| 锁文件 | `uv.lock` | 无原生对应（gradle lockfile 可选） |
| 包管理工具 | pip / uv | Maven / Gradle |
| 包目录标记 | `__init__.py` | 无需标记，目录即包 |
| 隔离环境 | venv / uv | JDK 版本 + 依赖作用域 |
| 运行入口 | `python -m` / `[project.scripts]` | `java -jar` / `main` 类 |

## 6. 今日练习（见 `base/day08/`）

1. 运行 `demo.py`，观察绝对/相对导入和 `__init__.py` 统一出口的效果
2. 完成 `work_pkg/core.py` 的 TODO，使 `work.py` 的全部断言通过
3. 口述：`pyproject.toml` 和 `uv.lock` 各负责什么？为什么 `.venv` 不进 Git？
