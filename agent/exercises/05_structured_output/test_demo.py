from __future__ import annotations

import json
import unittest

from .demo import (
    LABEL_CATALOG,
    VALID_MODEL_OUTPUT,
    DslValidationError,
    compile_interface_dsl,
    validate_model_output,
)


class StructuredOutputTests(unittest.TestCase):
    def payload(self) -> dict:
        return json.loads(VALID_MODEL_OUTPUT)

    def assert_error_code(self, payload: object, code: str) -> None:
        raw_text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        with self.assertRaises(DslValidationError) as context:
            validate_model_output(raw_text, LABEL_CATALOG, "test-trace")
        self.assertEqual(context.exception.code, code)
        self.assertEqual(context.exception.trace_id, "test-trace")

    def test_valid_output_can_be_compiled(self) -> None:
        selection = validate_model_output(VALID_MODEL_OUTPUT, LABEL_CATALOG, "ok")
        dsl = compile_interface_dsl(selection)
        self.assertEqual(dsl["showName"], "上海30岁以上女性")
        self.assertEqual(dsl["conditionGroups"][0]["rules"][1]["values"], [30])

    def test_invalid_json_is_rejected(self) -> None:
        self.assert_error_code("```json\n{}\n```", "MODEL_OUTPUT_INVALID_JSON")

    def test_extra_field_is_rejected(self) -> None:
        payload = self.payload()
        payload["unexpected"] = True
        self.assert_error_code(payload, "MODEL_OUTPUT_SCHEMA_ERROR")

    def test_string_is_not_coerced_to_number(self) -> None:
        payload = self.payload()
        payload["result"]["groups"][0]["rules"][1]["values"] = ["30"]
        self.assert_error_code(payload, "INVALID_NUMERIC_VALUE")

    def test_unknown_label_is_rejected(self) -> None:
        payload = self.payload()
        payload["result"]["groups"][0]["rules"][0]["label_id"] = "unknown"
        self.assert_error_code(payload, "UNKNOWN_LABEL")

    def test_incompatible_operator_is_rejected(self) -> None:
        payload = self.payload()
        payload["result"]["groups"][0]["rules"][1]["operator"] = "IN"
        self.assert_error_code(payload, "OPERATOR_NOT_ALLOWED")

    def test_expression_group_must_match_actual_groups(self) -> None:
        payload = self.payload()
        payload["conditionGroupsExpression"] = "((A2))"
        self.assert_error_code(payload, "EXPRESSION_GROUP_MISMATCH")

    def test_output_type_must_match_content(self) -> None:
        payload = self.payload()
        payload["label_select_output_type"] = 2
        payload["label_select_deficiency_reason"] = "没有对应标签"
        self.assert_error_code(payload, "OUTPUT_TYPE_INCONSISTENT")

    def test_unfulfillable_output_can_be_valid(self) -> None:
        payload = self.payload()
        payload["label_select_output_type"] = 2
        payload["label_select_deficiency_reason"] = "标签目录中没有相关标签"
        payload["audience_name"] = ""
        payload["result"]["groups"] = []
        payload["conditionGroupsExpression"] = ""
        selection = validate_model_output(
            json.dumps(payload, ensure_ascii=False), LABEL_CATALOG, "unfulfillable"
        )
        self.assertEqual(selection.label_select_output_type, 2)


if __name__ == "__main__":
    unittest.main()
