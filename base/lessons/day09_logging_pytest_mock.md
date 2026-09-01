# Day 9 — logging、pytest、fixture 与 Mock

> 日期：2026-07-29 | 预计用时：2 小时

---

## 1. logging：替代 print 的正确姿势

`print` 只能输出到终端、没有级别、生产无法收集。logging 解决这三件事：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("audience.service")  # 按模块起名，形成层级

logger.debug("调试细节，默认不输出")
logger.info("圈人请求已提交")
logger.warning("缺少城市条件，使用默认值")
logger.error("模型接口调用失败", exc_info=True)   # exc_info=True 打印堆栈
```

| 级别 | 用途 |
|------|------|
| DEBUG | 开发调试细节 |
| INFO | 关键流程节点（请求开始/结束） |
| WARNING | 可恢复的异常（降级、重试） |
| ERROR | 失败，需要关注 |
| CRITICAL | 服务级故障 |

两条军规：

1. **只在程序入口配置一次**（`basicConfig` 或 handler），库里只 `getLogger(__name__)`
2. **日志用占位符**：`logger.info("耗时 %s 秒", cost)`，不要 f-string——级别被过滤时不做字符串拼接，省性能

## 2. pytest：Python 的测试标准

```python
# test_xxx.py（文件名和函数名都以 test 开头才会被发现）
def test_age_condition():
    assert build_age_condition(18).op == ">="

# 运行
# pytest base/day09 -v          跑指定目录
# pytest -k summary             按名字过滤
# pytest -x                       遇到第一个失败就停
```

对比 unittest：不用继承类、直接 `assert`，失败信息自动展示两边值。

### 2.1 参数化：一个用例跑多组数据

```python
import pytest

@pytest.mark.parametrize("raw, expected", [
    ("hangzhou,shanghai", ["hangzhou", "shanghai"]),
    (" hangzhou , ", ["hangzhou"]),
])
def test_parse_city(raw, expected):
    assert parse_city_filter(raw) == expected

def test_empty_raises():
    with pytest.raises(ValueError):
        parse_city_filter(",,")
```

### 2.2 fixture：测试的"脚手架"

```python
import pytest

@pytest.fixture
def sample_request():
    """可复用的测试数据；每个用例拿到的都是新对象。"""
    return AudienceRequest(request_id="t-1", conditions=[...])

def test_summary(sample_request):        # 参数名 = fixture 名
    assert "AND" in sample_request.summary()
```

内置常用 fixture：`tmp_path`（临时目录）、`monkeypatch`（临时改环境）。

## 3. Mock：把"模型接口"换成假的

测试不能真的调模型接口（慢、花钱、不稳定）。Mock 的思路：**找到代码调用外部世界的边界，用假对象顶替**。

```python
from unittest.mock import patch, MagicMock

fake_model = MagicMock(return_value='{"age": ">=18"}')

# patch 的目标是"名字在被使用的地方"，不是定义的地方
with patch("my_module.call_model", fake_model):
    result = my_module.generate_audience("圈 18 岁以上")

fake_model.assert_called_once_with("圈 18 岁以上")   # 验证调用方式
```

三个要点：

1. `return_value`：固定返回值；`side_effect=[...]`：按顺序多次返回；`side_effect=ValueError("x")`：模拟抛异常
2. **patch 路径 = 被测代码 import 的位置**。`from x import y` 后要 patch `被测模块.y`
3. 断言调用：`assert_called_once_with` / `call_count`——既验证结果，也验证过程

## 4. Python vs Java 对比

| 特性 | Python | Java |
|------|--------|------|
| 日志门面 | `logging`（内置） | SLF4J + Logback |
| 测试框架 | pytest / unittest | JUnit |
| 参数化 | `@pytest.mark.parametrize` | `@ParameterizedTest` |
| 脚手架 | `@pytest.fixture` | `@BeforeEach` / `@Mock` |
| Mock | `unittest.mock`（内置） | Mockito |

## 5. 常见错误清单

```python
# ❌ 用 f-string 打日志
logger.info(f"耗时 {cost}")
# ✅ logger.info("耗时 %s", cost)

# ❌ patch 定义处而不是使用处，替换不生效

# ❌ 测试里 sleep 等真实网络——慢且不稳定，该 Mock 就 Mock

# ❌ 一个测试函数塞十个断言——失败时定位困难，拆开写
```

## 6. 今日练习

1. 运行 `demo.py`，观察日志格式与 Mock 替换效果
2. 阅读 `test_day06_generator.py`——它给 Day 6 的条件生成器补了测试（含 fixture 和 Mock）
3. 运行：`uv run pytest base/day09 -v`
4. 完成 `work.py` 的 TODO 测试，使 `uv run pytest base/day09/work.py -v` 全绿
