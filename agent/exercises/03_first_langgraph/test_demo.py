"""第 3 课参考实现测试。"""

import importlib.util
from pathlib import Path
import unittest


DEMO_PATH = Path(__file__).with_name("demo.py")
SPEC = importlib.util.spec_from_file_location("lesson_03_demo", DEMO_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载练习模块: {DEMO_PATH}")

demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class LangGraphWorkflowTest(unittest.TestCase):
    def test_audience_route(self) -> None:
        result = demo.graph.invoke(
            {"trace_id": "test-audience", "query": "帮我圈选女性用户"}
        )
        self.assertEqual(result["intent"], "audience")
        self.assertEqual(result["message"], "已进入圈人处理流程。")

    def test_non_audience_route(self) -> None:
        result = demo.graph.invoke(
            {"trace_id": "test-non-audience", "query": "今天天气怎么样"}
        )
        self.assertEqual(result["intent"], "non_audience")
        self.assertEqual(result["message"], "该请求不是圈人需求。")

    def test_empty_query_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(demo.WorkflowError, "MISSING_REQUIRED_FIELD"):
            demo.graph.invoke({"trace_id": "test-empty", "query": ""})

    def test_wrong_query_type_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(demo.WorkflowError, "MISSING_REQUIRED_FIELD"):
            demo.graph.invoke({"trace_id": "test-type", "query": 123})


if __name__ == "__main__":
    unittest.main()
