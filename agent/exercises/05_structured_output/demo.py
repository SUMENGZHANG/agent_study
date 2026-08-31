"""Strictly validate an LLM plan, then compile it to an interface DSL."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class DslValidationError(ValueError):
    """A stable, traceable validation failure safe for the graph boundary."""

    def __init__(self, code: str, message: str, trace_id: str) -> None:
        super().__init__(f"[{code}] {message} (trace_id={trace_id})")
        self.code = code
        self.message = message
        self.trace_id = trace_id


class Rule(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    label_id: str = Field(min_length=1)
    label_name: str = Field(min_length=1)
    label_type: Literal[0, 1, 2, 4]
    operator: str = Field(min_length=1)
    values: list[str | int | float] = Field(min_length=1)


class ConditionGroup(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    groupId: str = Field(pattern=r"^[A-Z][1-9][0-9]*$")
    entityId: str = Field(min_length=1)
    groupLogic: Literal["INTERSECTION", "UNION"]
    nextGroupRelation: Literal["INTERSECTION", "UNION", "EXCEPT"]
    rules: list[Rule] = Field(min_length=1)


class SelectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    groups: list[ConditionGroup]


class LabelSelection(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    label_select_output_type: Literal[0, 1, 2]
    label_select_deficiency_reason: str
    audience_name: str
    result: SelectionResult
    conditionGroupsExpression: str


@dataclass(frozen=True)
class LabelDefinition:
    name: str
    label_type: Literal[0, 1, 2, 4]
    allowed_operators: frozenset[str]
    allowed_values: frozenset[str] | None = None


LABEL_CATALOG: dict[str, LabelDefinition] = {
    "age": LabelDefinition(
        name="年龄",
        label_type=2,
        allowed_operators=frozenset(
            {"GREATER_THAN", "GREATER_THAN_OR_EQUAL", "LESS_THAN", "BETWEEN_AND"}
        ),
    ),
    "gender": LabelDefinition(
        name="性别",
        label_type=0,
        allowed_operators=frozenset({"EQUAL", "IN"}),
        allowed_values=frozenset({"男", "女"}),
    ),
    "city": LabelDefinition(
        name="常驻城市",
        label_type=0,
        allowed_operators=frozenset({"EQUAL", "IN"}),
        allowed_values=frozenset({"上海", "北京", "广州", "深圳"}),
    ),
}


def parse_model_output(raw_text: str, trace_id: str) -> LabelSelection:
    """Perform JSON syntax validation followed by strict schema validation."""
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise DslValidationError(
            "MODEL_OUTPUT_EMPTY", "模型输出必须是非空字符串", trace_id
        )

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise DslValidationError(
            "MODEL_OUTPUT_INVALID_JSON",
            f"模型输出不是合法 JSON：line={exc.lineno}, column={exc.colno}",
            trace_id,
        ) from exc

    try:
        return LabelSelection.model_validate(payload, strict=True)
    except ValidationError as exc:
        raise DslValidationError(
            "MODEL_OUTPUT_SCHEMA_ERROR", exc.json(), trace_id
        ) from exc


def _extract_expression_group_ids(expression: str, trace_id: str) -> list[str]:
    normalized = expression.strip()
    grammar = r"^\(\([A-Z][1-9][0-9]*\)(?: (?:AND|OR|EXCEPT) \([A-Z][1-9][0-9]*\))*\)$"
    if re.fullmatch(grammar, normalized) is None:
        raise DslValidationError(
            "EXPRESSION_SYNTAX_ERROR",
            "表达式必须形如 ((A1) AND (A2))",
            trace_id,
        )
    return re.findall(r"\(([A-Z][1-9][0-9]*)\)", normalized)


def _validate_rule(
    rule: Rule, catalog: dict[str, LabelDefinition], trace_id: str
) -> None:
    definition = catalog.get(rule.label_id)
    if definition is None:
        raise DslValidationError(
            "UNKNOWN_LABEL", f"标签不存在：{rule.label_id}", trace_id
        )
    if rule.label_name != definition.name or rule.label_type != definition.label_type:
        raise DslValidationError(
            "LABEL_METADATA_MISMATCH",
            f"标签元数据与目录不一致：{rule.label_id}",
            trace_id,
        )
    if rule.operator not in definition.allowed_operators:
        raise DslValidationError(
            "OPERATOR_NOT_ALLOWED",
            f"标签 {rule.label_id} 不支持操作符 {rule.operator}",
            trace_id,
        )

    if definition.label_type == 2:
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in rule.values):
            raise DslValidationError(
                "INVALID_NUMERIC_VALUE",
                f"数值标签 {rule.label_id} 的 values 必须全部是数值",
                trace_id,
            )
        if rule.operator == "BETWEEN_AND" and len(rule.values) != 2:
            raise DslValidationError(
                "INVALID_VALUE_COUNT", "BETWEEN_AND 必须恰好有两个值", trace_id
            )

    if definition.allowed_values is not None:
        invalid_values = [
            value
            for value in rule.values
            if not isinstance(value, str) or value not in definition.allowed_values
        ]
        if invalid_values:
            raise DslValidationError(
                "ENUM_VALUE_NOT_ALLOWED",
                f"标签 {rule.label_id} 包含非法枚举值：{invalid_values}",
                trace_id,
            )


def validate_business_rules(
    selection: LabelSelection,
    catalog: dict[str, LabelDefinition],
    trace_id: str,
) -> None:
    """Validate facts Pydantic cannot know, such as the live label catalog."""
    groups = selection.result.groups
    if selection.label_select_output_type == 0:
        if (
            not groups
            or selection.label_select_deficiency_reason
            or not selection.audience_name.strip()
        ):
            raise DslValidationError(
                "OUTPUT_TYPE_INCONSISTENT",
                "完全实现时必须有条件组和人群名称，且缺失原因必须为空",
                trace_id,
            )
    elif selection.label_select_output_type == 1:
        if (
            not groups
            or not selection.label_select_deficiency_reason.strip()
            or not selection.audience_name.strip()
        ):
            raise DslValidationError(
                "OUTPUT_TYPE_INCONSISTENT",
                "部分实现时必须有条件组、人群名称和缺失原因",
                trace_id,
            )
    elif (
        groups
        or not selection.label_select_deficiency_reason.strip()
        or selection.audience_name
        or selection.conditionGroupsExpression not in ("", "()")
    ):
        raise DslValidationError(
            "OUTPUT_TYPE_INCONSISTENT",
            "完全无法实现时条件组和人群名称必须为空，且必须说明原因",
            trace_id,
        )

    group_ids = [group.groupId for group in groups]
    if len(group_ids) != len(set(group_ids)):
        raise DslValidationError("DUPLICATE_GROUP_ID", "条件组 ID 不允许重复", trace_id)

    if selection.label_select_output_type == 2:
        return

    expression_ids = _extract_expression_group_ids(selection.conditionGroupsExpression, trace_id)
    if len(expression_ids) != len(set(expression_ids)):
        raise DslValidationError(
            "DUPLICATE_EXPRESSION_GROUP", "表达式不允许重复引用条件组", trace_id
        )
    if set(expression_ids) != set(group_ids):
        raise DslValidationError(
            "EXPRESSION_GROUP_MISMATCH",
            f"表达式分组 {expression_ids} 与实际分组 {group_ids} 不一致",
            trace_id,
        )

    for group in groups:
        for rule in group.rules:
            _validate_rule(rule, catalog, trace_id)


def validate_model_output(
    raw_text: str,
    catalog: dict[str, LabelDefinition],
    trace_id: str,
) -> LabelSelection:
    selection = parse_model_output(raw_text, trace_id)
    validate_business_rules(selection, catalog, trace_id)
    return selection


def compile_interface_dsl(selection: LabelSelection) -> dict[str, object]:
    """Deterministically map an already-validated plan to the downstream DSL."""
    condition_groups = []
    for group in selection.result.groups:
        condition_groups.append(
            {
                "type": "LABEL",
                "relation": group.groupLogic,
                "nextRelation": group.nextGroupRelation,
                "entityId": group.entityId,
                "conditionGroupId": group.groupId,
                "rules": [
                    {
                        "labelId": rule.label_id,
                        "labelName": rule.label_name,
                        "labelType": rule.label_type,
                        "operator": rule.operator,
                        "values": list(rule.values),
                    }
                    for rule in group.rules
                ],
            }
        )

    return {
        "showName": selection.audience_name,
        "parentId": "0",
        "isUpdate": True,
        "entityId": "-1",
        "conditionGroups": condition_groups,
        "conditionGroupsExpression": selection.conditionGroupsExpression,
    }


VALID_MODEL_OUTPUT = json.dumps(
    {
        "label_select_output_type": 0,
        "label_select_deficiency_reason": "",
        "audience_name": "上海30岁以上女性",
        "result": {
            "groups": [
                {
                    "groupId": "A1",
                    "entityId": "user",
                    "groupLogic": "INTERSECTION",
                    "nextGroupRelation": "INTERSECTION",
                    "rules": [
                        {
                            "label_id": "city",
                            "label_name": "常驻城市",
                            "label_type": 0,
                            "operator": "EQUAL",
                            "values": ["上海"],
                        },
                        {
                            "label_id": "age",
                            "label_name": "年龄",
                            "label_type": 2,
                            "operator": "GREATER_THAN_OR_EQUAL",
                            "values": [30],
                        },
                        {
                            "label_id": "gender",
                            "label_name": "性别",
                            "label_type": 0,
                            "operator": "EQUAL",
                            "values": ["女"],
                        },
                    ],
                }
            ]
        },
        "conditionGroupsExpression": "((A1))",
    },
    ensure_ascii=False,
)


if __name__ == "__main__":
    validated = validate_model_output(VALID_MODEL_OUTPUT, LABEL_CATALOG, "demo-001")
    print(json.dumps(compile_interface_dsl(validated), ensure_ascii=False, indent=2))
