"""
Day 8 工程化速查笔记

对应课程：lessons/day08_project_packaging_uv_pyproject.md
先凭理解填 TODO，再对照课程查漏。
"""

# ==================== 1. 虚拟环境 ====================

# TODO: 为什么每个项目要独立虚拟环境？

# TODO: 写出创建并激活 venv 的命令（传统方式）

# TODO: 写出 uv 的三个常用命令：建环境、加依赖、运行脚本


# ==================== 2. pyproject.toml ====================

# TODO: dependencies 和 dev 依赖组的区别是什么？

# TODO: pyproject.toml 和 uv.lock 各负责什么？哪个不进 Git？
#   （提示：.venv 不进，锁文件要进）


# ==================== 3. 包结构 ====================

# TODO: 目录变成"包"需要什么文件？它还能承担什么职责？
#   （提示：__init__.py，统一出口 / __all__）

# TODO: 包内模块之间用什么导入？外部使用包用什么导入？


# ==================== 4. import 与 sys.path ====================

# TODO: import 时 Python 按什么顺序查找模块？

# TODO: ModuleNotFoundError 的三种常见原因？

# TODO: 为什么 python pkg/mod.py 直接跑包内文件会报相对导入错误？


# ==================== 5. 今日核心一句话 ====================
#
# 虚拟环境隔离依赖，.venv 不进 Git，锁文件要进
# pyproject.toml 声明要什么，uv.lock 锁定具体版本
# __init__.py 让目录成为包，并做统一出口
# 包内相对导入，外部绝对导入
# 报错先查 which python 和 sys.path
