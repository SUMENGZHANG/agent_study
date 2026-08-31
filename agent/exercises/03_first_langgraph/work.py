"""第 3 课练习：把手写 Runner 迁移成真正的 LangGraph。"""
import json
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    trace_id: str
    query: str
    intent: str
    message: str


def recognize_intent(state: AgentState) -> dict[str, Any]:
    """严格校验输入，返回 audience 或 non_audience。"""
    query = state.get("query")
    if query is None:
        raise ValueError("Missing query")
    if "圈" in query:
        return {"intent": "audience"}
    return {"intent": "non_audience"}

    raise NotImplementedError("请实现 recognize_intent")


def route_after_intent(
    state: AgentState,
) -> Literal["continue", "finish"]:
    """根据 intent 返回路由 Key，未知 intent 必须明确失败。"""
    intent = state.get("intent")
    if intent == "audience":
        return "continue"
    if intent == "non_audience":
        return "finish"
    raise NotImplementedError("请实现 route_after_intent")


def audience_node(state: AgentState) -> dict[str, Any]:
    """圈人分支的结束节点。"""
    return {"message": "已圈选女性用户"}
    raise NotImplementedError("请实现 audience_node")


def non_audience_node(state: AgentState) -> dict[str, Any]:

    """非圈人分支的结束节点。"""
    return {"message": "已拒绝"}
    raise NotImplementedError("请实现 non_audience_node")


def build_graph():
    """注册节点和边，编译并返回可执行 Graph。"""
    graph = StateGraph(AgentState)
    """注册node"""
    graph.add_node("recognize_intent", recognize_intent)
    graph.add_node("audience_node", audience_node)
    graph.add_node("non_audience_node", non_audience_node)
    """注册edge"""
    graph.add_edge(START, "recognize_intent")
    graph.add_conditional_edges(
        "recognize_intent",
        route_after_intent,
        {
            "continue": "audience_node",
            "finish": "non_audience_node",
        },
    )
    graph.add_edge("audience_node", END)
    graph.add_edge("non_audience_node", END)
    return graph.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke(
        {
            "trace_id": "lesson-03-work",
            "query": "帮我圈选女性用户",
        }
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
