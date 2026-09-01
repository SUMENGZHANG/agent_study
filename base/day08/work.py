"""Day 8 练习：搭建一个规范的小包（核心代码在 work_pkg/core.py，约 20 行）。

步骤：
1. 观察 demo_pkg/ 的三个文件：__init__.py（统一出口）、models.py、services.py
2. 实现 work_pkg/core.py 的两个 TODO 函数
3. 运行本文件：python work.py，全部断言通过即完成
"""
from __future__ import annotations

from work_pkg import build_condition_dict, validate_age_range


def main() -> None:
    # ---- validate_age_range ----
    validate_age_range(None, None)          # 全不限制：合法
    validate_age_range(18, None)            # 只限制下限：合法
    validate_age_range(None, 60)            # 只限制上限：合法
    validate_age_range(18, 35)              # 正常区间：合法

    for bad_args in [(-1, None), (None, -5), (35, 18)]:
        try:
            validate_age_range(*bad_args)
        except ValueError as exc:
            print(f"  正确拦截非法区间 {bad_args}: {exc}")
        else:
            raise AssertionError(f"非法区间 {bad_args} 未被拦截")

    # ---- build_condition_dict ----
    cond = build_condition_dict("age", ">=", 18)
    assert cond == {"field_name": "age", "op": ">=", "value": 18}

    for bad_field, bad_op in [("", ">="), ("age", "LIKE")]:
        try:
            build_condition_dict(bad_field, bad_op, 18)
        except ValueError as exc:
            print(f"  正确拦截非法条件 ({bad_field!r}, {bad_op!r}): {exc}")
        else:
            raise AssertionError(f"非法条件 ({bad_field!r}, {bad_op!r}) 未被拦截")

    print("全部断言通过 ✔")


if __name__ == "__main__":
    main()
