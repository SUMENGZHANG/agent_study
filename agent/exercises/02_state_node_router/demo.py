"""不用 LangGraph，手动模拟 State、Node、Edge 和 Router。"""

from __future__ import annotations

import json
import re
from typing import Any, Callable, TypedDict


class AgentState(TypedDict, total=False):
    trace_id: str
    query: str
    intent: str
    dimensions: dict[str, Any]
    result: dict[str, Any]
    message: str
    route: str


class WorkflowError(RuntimeError):
    """包含稳定错误码和 trace_id 的工作流异常。"""

    def __init__(self, code: str, message: str, trace_id: str) -> None:
        super().__init__(f"[{code}] {message} (trace_id={trace_id})")
        self.code = code
        self.trace_id = trace_id


Node = Callable[[AgentState], dict[str, Any]]


def require_text(state: AgentState, field: str) -> str:
    trace_id = state.get("trace_id")
    if not isinstance(trace_id, str) or not trace_id.strip():
        raise WorkflowError("MISSING_TRACE_ID", "trace_id 是必需字段", "unknown")

    value = state.get(field)
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError(
            "MISSING_REQUIRED_FIELD",
            f"{field} 必须是非空字符串",
            trace_id,
        )
    return value.strip()


def recognize_intent(state: AgentState) -> dict[str, Any]:
    query = require_text(state, "query")
    if "圈选" in query or "筛选" in query:
        return {"intent": "audience"}
    return {"intent": "non_audience"}


def route_after_intent(state: AgentState) -> str:
    trace_id = require_text(state, "trace_id")
    intent = state.get("intent")
    if intent == "audience":
        return "continue"
    if intent == "non_audience":
        return "finish"
    raise WorkflowError(
        "INVALID_INTENT",
        f"未声明的意图: {intent!r}",
        trace_id,
    )


def extract_dimensions(state: AgentState) -> dict[str, Any]:
    trace_id = require_text(state, "trace_id")
    query = require_text(state, "query")
    dimensions: dict[str, Any] = {}

    age_match = re.search(r"(\d+)岁以上", query)
    if age_match:
        dimensions["age_min"] = int(age_match.group(1))

    if "女性" in query:
        dimensions["gender"] = "female"
    elif "男性" in query:
        dimensions["gender"] = "male"

    if not dimensions:
        raise WorkflowError(
            "DIMENSION_NOT_FOUND",
            "没有识别到本练习支持的年龄或性别维度",
            trace_id,
        )
    return {"dimensions": dimensions}


def build_result(state: AgentState) -> dict[str, Any]:
    trace_id = require_text(state, "trace_id")
    dimensions = state.get("dimensions")
    if not isinstance(dimensions, dict) or not dimensions:
        raise WorkflowError(
            "MISSING_DIMENSIONS",
            "生成结果前必须存在 dimensions",
            trace_id,
        )
    return {
        "result": {
            "type": "audience_filter",
            "conditions": dimensions.copy(),
        }
    }


def finish_non_audience(state: AgentState) -> dict[str, Any]:
    require_text(state, "trace_id")
    return {"message": "该请求不是圈人需求。"}


def run_workflow(initial_state: AgentState) -> AgentState:
    """按照固定 Graph 执行，并显式合并每个 Node 的增量输出。"""
    state: AgentState = dict(initial_state)

    delta = recognize_intent(state)
    state.update(delta)

    route = route_after_intent(state)
    state["route"] = route

    path_map: dict[str, tuple[Node, ...]] = {
        "continue": (extract_dimensions, build_result),
        "finish": (finish_non_audience,),
    }
    if route not in path_map:
        trace_id = require_text(state, "trace_id")
        raise WorkflowError(
            "ROUTE_NOT_MAPPED",
            f"路由未配置: {route}",
            trace_id,
        )

    for node in path_map[route]:
        delta = node(state)
        state.update(delta)

    return state


if __name__ == "__main__":
    final_state = run_workflow(
        {
            "trace_id": "lesson-02-demo",
            "query": "帮我圈选30岁以上的女性用户",
        }
    )
    print(json.dumps(final_state, ensure_ascii=False, indent=2))
