# 第 3 课：第一个真正的 LangGraph

## 本课目标

- 把上一课的手写 Runner 迁移到 LangGraph。
- 理解 Graph Builder 和 Compiled Graph 的区别。
- 使用 `START`、`END`、`add_node`、`add_conditional_edges`。
- 使用 `invoke()` 执行 Graph。

## 1. 手写 Runner 与 LangGraph 的对应关系

上一课手写了：

```text
调用 Node
→ 合并 delta
→ 调用 Router
→ 查询 PATH_MAP
→ 调用下一个 Node
```

LangGraph 帮我们完成的正是这部分调度：

| 手写实现 | LangGraph |
|---|---|
| `state.update(delta)` | 自动合并节点返回值 |
| `PATH_MAP` | `add_conditional_edges(..., path_map)` |
| 手动调用函数 | `add_node` 注册后由运行时调用 |
| 自己决定入口 | `START` 或 `set_entry_point` |
| 自己结束函数调用 | `END` |
| `run_workflow(state)` | `graph.invoke(state)` |

## 2. Graph Builder 不能直接执行

```python
builder = StateGraph(AgentState)
```

`builder` 用来描述结构。完成节点和边的注册后，需要编译：

```python
graph = builder.compile()
```

编译阶段会检查部分结构问题，并生成可以 `invoke()`、`stream()` 或异步执行的 Compiled Graph。

## 3. 注册节点

```python
builder.add_node("recognize_intent", recognize_intent)
```

这里只是把名称与函数登记到 Graph，没有立即执行函数。

节点契约仍然是：

```text
State → Partial State
```

也就是读取完整 State，返回部分更新。

## 4. 添加固定 Edge

```python
builder.add_edge(START, "recognize_intent")
builder.add_edge("audience_node", END)
```

- `START` 是特殊入口标记。
- `END` 是特殊结束标记。
- `es-ai master` 使用的 `set_entry_point("意图识别")` 与从 `START` 添加边表达相同目的。

## 5. 添加条件 Edge

```python
builder.add_conditional_edges(
    "recognize_intent",
    route_after_intent,
    {
        "continue": "audience_node",
        "finish": "non_audience_node",
    },
)
```

执行顺序：

```text
recognize_intent 返回 {"intent": "audience"}
→ LangGraph 合并 State
→ route_after_intent 读取更新后的 State
→ 返回 "continue"
→ path_map 映射到 audience_node
```

给 Router 标注 `Literal` 可以让允许的路由结果更加清晰：

```python
def route_after_intent(state: AgentState) -> Literal["continue", "finish"]:
    ...
```

## 6. 编译与执行

```python
graph = builder.compile()

result = graph.invoke(
    {
        "trace_id": "lesson-03",
        "query": "帮我圈选女性用户",
    }
)
```

`invoke()` 返回最终 State，而不是只返回最后一个节点的结果。

## 7. 配套文件

- `demo.py`：完整参考实现。
- `work.py`：你的迁移练习。
- `test_demo.py`：参考实现测试。

目录：

```text
agent/exercises/03_first_langgraph/
```

运行：

```bash
cd /Users/sumengzhang/Desktop/projects/agent_study
uv run python agent/exercises/03_first_langgraph/demo.py
uv run python -m unittest agent/exercises/03_first_langgraph/test_demo.py
```

## 8. 练习要求

在 `work.py` 中完成：

1. 严格校验 `trace_id` 和 `query`。
2. 实现意图识别 Node。
3. 实现 Router，未知意图明确失败。
4. 注册两个结束分支 Node。
5. 用 `START`、条件 Edge、`END` 构建 Graph。
6. 编译并通过 `invoke()` 执行。

禁止在 Graph 外再手写 `state.update()` 或 PATH_MAP 调度；这次要让 LangGraph 接管它们。

## 本课完成标准

能够用自己的话解释：

1. `StateGraph` 和 `compile()` 后的 Graph 有什么区别？
2. Node 是注册时执行，还是 `invoke()` 时执行？
3. Router 读取的是节点执行前还是合并后的 State？
4. `invoke()` 为什么返回完整最终 State？
