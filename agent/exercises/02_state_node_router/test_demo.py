"""参考实现测试。"""

import importlib.util
from pathlib import Path
import unittest


DEMO_PATH = Path(__file__).with_name("demo.py")
SPEC = importlib.util.spec_from_file_location("lesson_02_demo", DEMO_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载练习模块: {DEMO_PATH}")

demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class WorkflowTest(unittest.TestCase):
    def test_audience_request(self) -> None:
        state = demo.run_workflow(
            {
                "trace_id": "test-audience",
                "query": "帮我圈选30岁以上的女性用户",
            }
        )
        self.assertEqual(state["route"], "continue")
        self.assertEqual(state["result"]["conditions"]["age_min"], 30)
        self.assertEqual(state["result"]["conditions"]["gender"], "female")

    def test_non_audience_request(self) -> None:
        state = demo.run_workflow(
            {"trace_id": "test-non-audience", "query": "今天天气怎么样"}
        )
        self.assertEqual(state["route"], "finish")
        self.assertEqual(state["message"], "该请求不是圈人需求。")
        self.assertNotIn("result", state)

    def test_missing_query_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(demo.WorkflowError, "MISSING_REQUIRED_FIELD"):
            demo.run_workflow({"trace_id": "test-missing-query"})

    def test_unsupported_dimension_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(demo.WorkflowError, "DIMENSION_NOT_FOUND"):
            demo.run_workflow(
                {"trace_id": "test-no-dimension", "query": "帮我圈选高价值客户"}
            )


if __name__ == "__main__":
    unittest.main()
