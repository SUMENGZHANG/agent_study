"""第 2 课练习：完成一个最小条件路由工作流。"""

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    query: str
    intent: str
    message: str


def recognize_intent(state: AgentState) -> dict[str, Any]:
    """根据 query 返回 intent：audience 或 non_audience。"""

    query = state.get("query")
    if query is None:
        raise ValueError("Missing query")
    if "圈" in query:
        return {"intent": "audience"}
    return {"intent": "non_audience"}


def route_after_intent(state: AgentState) -> str:
    """返回 continue 或 finish；未知 intent 必须明确报错。"""
    intent = state.get("intent")
    if intent == "audience":
        return "continue"
    if intent == "non_audience":
        return "finish"

    raise ValueError(f"Unknown intent: {intent}")


def follow_node(state: AgentState) -> dict[str, Any]:
    """continue 分支：生成追问消息。"""
    return {"message": "请提供更多信息。"}


def end_node(state: AgentState) -> dict[str, Any]:
    """finish 分支：生成结束消息。"""
    return {"message": "感谢使用。"}


PATH_MAP = {
    "continue": follow_node,
    "finish": end_node,
}


def run_workflow(initial_state: AgentState) -> AgentState:
    """执行意图节点、合并增量、选择路径并生成最终 message。"""
    delta = recognize_intent(initial_state)
    initial_state.update(delta)

    route = route_after_intent(initial_state)
    node = PATH_MAP.get(route)
    if node is None:
        raise ValueError(f"Unknown route: {route}")

    delta = node(initial_state)
    initial_state.update(delta)
    return initial_state


if __name__ == '__main__':
    query = '帮我圈一个人'
    state = AgentState(query=query)
    print(state)
    result = run_workflow(state)
    print(result)

