"""第一个真正的 LangGraph：意图识别与条件路由。"""

from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    trace_id: str
    query: str
    intent: str
    message: str


class WorkflowError(RuntimeError):
    def __init__(self, code: str, message: str, trace_id: str) -> None:
        super().__init__(f"[{code}] {message} (trace_id={trace_id})")
        self.code = code
        self.trace_id = trace_id


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


def route_after_intent(
    state: AgentState,
) -> Literal["continue", "finish"]:
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


def audience_node(state: AgentState) -> dict[str, Any]:
    require_text(state, "trace_id")
    return {"message": "已进入圈人处理流程。"}


def non_audience_node(state: AgentState) -> dict[str, Any]:
    require_text(state, "trace_id")
    return {"message": "该请求不是圈人需求。"}


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("recognize_intent", recognize_intent)
    builder.add_node("audience_node", audience_node)
    builder.add_node("non_audience_node", non_audience_node)

    builder.add_edge(START, "recognize_intent")
    builder.add_conditional_edges(
        "recognize_intent",
        route_after_intent,
        {
            "continue": "audience_node",
            "finish": "non_audience_node",
        },
    )
    builder.add_edge("audience_node", END)
    builder.add_edge("non_audience_node", END)
    return builder.compile()


graph = build_graph()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "trace_id": "lesson-03-demo",
            "query": "帮我圈选女性用户",
        }
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
