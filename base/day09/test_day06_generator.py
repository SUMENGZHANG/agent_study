"""Day 9 示范测试：给 Day 6 的"圈人条件生成器"补单元测试。

运行：uv run pytest base/day09/test_day06_generator.py -v
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Day 6 的 demo.py 是脚本不是包，用 importlib 直接按文件加载。
# 注意：必须注册进 sys.modules，否则其内部的 @dataclass 解析注解会报错。
DEMO_PATH = Path(__file__).resolve().parents[1] / "day06" / "demo.py"
_spec = importlib.util.spec_from_file_location("day06_demo", DEMO_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"无法加载被测模块: {DEMO_PATH}")
day06 = importlib.util.module_from_spec(_spec)
sys.modules["day06_demo"] = day06
_spec.loader.exec_module(day06)


@pytest.fixture
def empty_args() -> argparse.Namespace:
    """模拟 parse_args() 的返回结构：未指定任何条件。"""
    return argparse.Namespace(
        min_age=None,
        max_age=None,
        gender=None,
        city=None,
        vip=False,
        logic="AND",
        output=None,
    )


def test_no_conditions_when_no_args(empty_args):
    assert day06.build_conditions(empty_args) == []


def test_age_range_generates_two_conditions(empty_args):
    empty_args.min_age = 18
    empty_args.max_age = 35
    conds = day06.build_conditions(empty_args)
    assert [(c.field_name, c.op, c.value) for c in conds] == [
        ("age", ">=", 18),
        ("age", "<=", 35),
    ]


def test_multiple_cities_generate_multiple_conditions(empty_args):
    empty_args.city = ["hangzhou", "shanghai"]
    conds = day06.build_conditions(empty_args)
    assert len(conds) == 2
    assert all(c.field_name == "city" for c in conds)


def test_vip_flag_appends_true_condition(empty_args):
    empty_args.vip = True
    conds = day06.build_conditions(empty_args)
    assert conds[-1].value is True


@pytest.fixture
def two_condition_request(empty_args):
    """fixture 可以复用组装逻辑：年龄下限 + 一个城市。"""
    empty_args.min_age = 18
    empty_args.city = ["hangzhou"]
    return day06.build_request(empty_args)


def test_summary_joined_with_and(two_condition_request):
    assert two_condition_request.summary() == "age >= 18 AND city == hangzhou"


def test_summary_joined_with_or(two_condition_request):
    two_condition_request.logic = "OR"
    assert " OR " in two_condition_request.summary()


def test_format_output_is_valid_json(two_condition_request):
    payload = json.loads(day06.format_output(two_condition_request))
    assert payload["logic"] == "AND"
    assert len(payload["conditions"]) == 2


def test_request_id_comes_from_uuid(empty_args):
    """Mock 外部依赖：uuid 是随机的，不 Mock 就没法写出确定断言。"""
    with patch.object(day06.uuid, "uuid4", return_value="ABCDEFGH-fake-id") as mock_uuid:
        empty_args.min_age = 1
        request = day06.build_request(empty_args)

    assert request.request_id == "ABCDEFGH"
    mock_uuid.assert_called_once()
