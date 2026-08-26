# 第 2 课：State、Node、Edge 与 Router

## 本课目标

- 理解 State 为什么是工作流的共享上下文。
- 理解 Node 读取 State、返回“增量更新”的模式。
- 区分普通 Edge 和 Conditional Edge。
- 看懂 Router 为什么返回路由 Key，而不是直接调用下一个节点。

## 1. State：一次运行中的共享数据

State 可以理解为一次 Agent Run 的工作台：

```python
state = {
    "trace_id": "run-001",
    "query": "帮我圈选30岁以上的女性用户",
}
```

随着节点执行，State 会逐步增加字段：

```python
{
    "trace_id": "run-001",
    "query": "帮我圈选30岁以上的女性用户",
    "intent": "audience",
    "dimensions": {"age_min": 30, "gender": "female"},
    "result": {...},
}
```

State 只在一次 Graph 运行中传递。它和跨请求保存的 Session Memory 不是同一个概念。

## 2. Node：读取完整 State，返回部分更新

一个 Node 通常不需要返回整个 State：

```python
def recognize_intent(state: AgentState) -> dict:
    query = state["query"]
    return {"intent": "audience"}
```

Runner 会把节点返回值合并回 State：

```python
delta = recognize_intent(state)
state.update(delta)
```

因此要区分：

- `state`：执行节点前已经积累的完整状态。
- `delta`：当前节点产生的增量结果。

## 3. Edge：固定的下一步

普通 Edge 表示无条件执行：

```text
提取维度 → 生成圈人结果
```

在 LangGraph 中类似：

```python
graph.add_edge("提取维度", "生成结果")
```

## 4. Router：根据 State 选择下一条路

Router 本质上是一个普通函数：

```python
def route_after_intent(state: AgentState) -> str:
    if state["intent"] == "audience":
        return "continue"
    if state["intent"] == "non_audience":
        return "finish"
    raise WorkflowError("INVALID_INTENT", "未声明的意图")
```

Router 返回的是路由 Key，再由 `path_map` 转成节点名：

```python
path_map = {
    "continue": "提取维度",
    "finish": "非圈人结束",
}
```

这样做的好处是 Router 只负责业务判断，不负责执行节点，流程结构仍由 Graph 统一管理。

## 5. 为什么不能给 Router 随意兜底

下面这种写法看似健壮，实际上会隐藏模型协议错误：

```python
return "finish"  # 所有未知意图都当成非圈人
```

如果模型错误返回 `"audinece"`，系统会把明确圈人需求误判为非圈人。正确做法是让未知状态明确失败，便于发现 Prompt 或响应协议问题。

## 6. 与 `es-ai master` 对照

阅读以下位置：

```text
/Users/sumengzhang/Desktop/projects/es-ai/Audience_Copilot/agent/graph.py
/Users/sumengzhang/Desktop/projects/es-ai/Audience_Copilot/nodes/route/agent_route_node.py
```

重点观察：

1. `AgentState` 中哪些字段属于输入、过程和输出。
2. 每个 `add_node` 注册的是函数，不是立即执行函数。
3. `add_edge` 描述固定路径。
4. `add_conditional_edges` 将 Router 返回值映射为节点。
5. `compile()` 后才得到可执行 Graph。

## 7. 配套代码

- `demo.py`：完整可运行参考实现。
- `work.py`：需要自己完成的练习。
- `test_demo.py`：验证正常、提前结束和失败路径。

目录：

```text
agent/exercises/02_state_node_router/
```

运行参考实现：

```bash
cd /Users/sumengzhang/Desktop/projects/agent_study
python3 agent/exercises/02_state_node_router/demo.py
python3 -m unittest agent/exercises/02_state_node_router/test_demo.py
```

## 本课完成标准

不看资料也能回答：

1. Node 为什么只返回部分 State？
2. `state.update(delta)` 在模拟什么？
3. Router 为什么不直接调用下一节点？
4. `path_map` 的 Key 和 Value 分别是什么？
5. 未知路由为什么应该报错？
