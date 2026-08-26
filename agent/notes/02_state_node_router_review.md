# 第 2 课 `work.py` 评审

## 已正确掌握

你已经完成了本课最重要的执行链：

```text
recognize_intent(state)
→ 返回 delta
→ state.update(delta)
→ route_after_intent(state)
→ PATH_MAP 选择 Node
→ Node 返回 delta
→ state.update(delta)
→ 返回最终 State
```

做得好的地方：

- Node 没有直接负责跳转，只返回 State 增量。
- Router 只返回 `continue` 或 `finish`。
- `PATH_MAP` 将路由 Key 与函数分离。
- 未知 intent 和未知 route 都会明确报错。
- 正常圈人和非圈人路径均可运行。

## 需要自己修改的三个问题

### 1. Query 校验不完整

当前只判断 `query is None`，所以空字符串会被当成非圈人请求：

```python
{"query": ""}
```

应要求 Query 必须是非空字符串。建议错误信息稳定、明确，例如：

```text
MISSING_QUERY: query 必须是非空字符串
```

### 2. 类型错误没有转成工作流错误

当前传入：

```python
{"query": 123}
```

会在 `"圈" in query` 处产生 Python `TypeError`。这不能清楚说明输入协议。应在进入业务判断前验证类型，并主动抛出带业务错误码的异常。

### 3. `"圈" in query` 规则过宽

下面的非圈人请求会被误判：

```text
我的朋友圈最近很热闹
```

初学练习可改为检测更明确的动作词，例如 `圈选` 或 `筛选`。这仍然只是规则模拟；真实项目使用模型识别意图，但模型输出也必须经过枚举校验。

## 额外思考：不要直接修改调用者传入的字典

当前 `run_workflow` 直接修改 `initial_state`。这不是本课错误，但可能让调用者意外发现自己的原始字典被改变。

可以在函数入口复制：

```python
state: AgentState = dict(initial_state)
```

后续都修改 `state`，最后返回 `state`。这也更接近“一次 Run 拥有自己的运行状态”的理解。

## 修改后的自测用例

至少验证：

1. `帮我圈选女性用户` → `audience`。
2. `今天天气怎么样` → `non_audience`。
3. 缺少 `query` → 明确错误。
4. `query=""` → 明确错误。
5. `query=123` → 明确错误，而不是原生 `TypeError`。
6. `我的朋友圈最近很热闹` → `non_audience`。

## 下一步

完成上述修改后，将这套手写 Runner 改为真正的 LangGraph：

```text
StateGraph
→ add_node
→ add_conditional_edges
→ compile
→ invoke
```

对照后会发现 LangGraph 主要替你完成了节点注册、路径调度和 State 合并。
