"""
Day 9 logging/pytest/Mock 速查笔记

对应课程：lessons/day09_logging_pytest_mock.md
先凭理解填 TODO，再对照课程查漏。
"""

# ==================== 1. logging ====================

# TODO: 写出 basicConfig 的 level 和 format 配置

# TODO: 五个日志级别从低到高排序

# TODO: 为什么日志推荐 %s 占位符而不是 f-string？


# ==================== 2. pytest ====================

# TODO: 测试文件和测试函数的命名规则是什么？

# TODO: 写出一个最简单的断言和用 pytest.raises 断言异常

# TODO: @pytest.mark.parametrize 解决什么问题？

# TODO: @pytest.fixture 的作用？参数名和函数名是什么关系？


# ==================== 3. Mock ====================

# TODO: 什么情况必须用 Mock？（提示：外部依赖的特征）

# TODO: MagicMock 的 return_value 和 side_effect 各适用什么场景？

# TODO: patch 的路径应该写"定义处"还是"使用处"？为什么？

# TODO: 怎样验证 mock 被调用的次数和参数？


# ==================== 4. 今日核心一句话 ====================
#
# print 换 logging：有级别、可收集、入口配置一次
# pytest：test_ 命名自动发现，assert 直接写，fixture 供数据
# 参数化一个用例多组数据，异常用 pytest.raises
# Mock 替换外部边界：patch 使用处，断言调用过程
