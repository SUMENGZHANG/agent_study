"""Day 9 练习：为给定函数编写 pytest 测试。

运行：uv run pytest base/day09/work.py -v
目标：把三个 TODO 测试实现出来，全部通过。
"""
from __future__ import annotations

import pytest


# ---------- 被测函数 1（已实现，你来写测试） ----------

def parse_city_filter(raw: str) -> list[str]:
    """把 "hangzhou,shanghai" 解析成城市列表。

    规则：
    1. 去掉每个城市名前后空白
    2. 丢弃空项
    3. 解析结果为空抛 ValueError
    4. 城市名包含数字抛 ValueError
    """
    cities = [item.strip() for item in raw.split(",") if item.strip()]
    if not cities:
        raise ValueError("城市列表不能为空")
    if any(ch.isdigit() for city in cities for ch in city):
        raise ValueError(f"城市名不能包含数字: {cities}")
    return cities


# TODO 1: 用 @pytest.mark.parametrize 写参数化测试，至少覆盖 5 组：
#   正常多城市 / 两侧空白 / 结尾多逗号 / 单城市 / 顺序保持不变
def test_parse_city_filter():
    raise NotImplementedError("请写参数化测试")


# TODO 2: 用 pytest.raises 分别验证 "" 和 "hangzhou2" 抛 ValueError
def test_parse_city_filter_rejects_bad_input():
    raise NotImplementedError("请写异常断言测试")


# ---------- 被测函数 2（依赖外部 fetcher，需要 Mock） ----------

def count_high_value_users(fetcher) -> int:
    """fetcher() 返回用户年龄列表，统计 18 岁及以上人数。

    fetcher 模拟标签服务接口——测试里用 MagicMock 替换，不能真调外部服务。
    """
    ages = fetcher()
    return sum(1 for age in ages if age >= 18)


# TODO 3: 用 MagicMock(return_value=[...]) 构造 fetcher，验证：
#   1. 计数结果正确
#   2. fetcher 恰好被调用一次（assert_called_once）
#   加分：再用 side_effect=ValueError("服务不可用") 验证异常会原样传播
def test_count_high_value_users_with_mock():
    raise NotImplementedError("请写 Mock 测试")
