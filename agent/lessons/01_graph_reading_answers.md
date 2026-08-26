# `graph.py` 第一遍阅读参考答案

参考源码：

```text
/Users/sumengzhang/Desktop/projects/es-ai/Audience_Copilot/agent/graph.py
```

## 1. 工作流的入口节点是什么？

入口是“意图识别”：

```python
graph.set_entry_point("意图识别")
```

每次调用 Graph 时，无论用户输入是不是圈人请求，都会先判断意图，再决定是否进入后续圈人流程。

## 2. 意图识别后有几条分支？

路由值有三种：

- `"1"`：明确圈人需求，进入 Query 改写。
- `"2"`：模糊圈人需求，进入非明确圈人结束节点。
- `"3"`：其他问题，进入非明确圈人结束节点。

从业务路径看，其实只有两条：继续生成圈人方案，或者提前结束。

需要留意：路由函数把所有非 `1`、非 `2` 的结果都当成 `3`。这是一种静默兜底。生产代码更合理的做法是：模型返回未声明值时抛出明确的意图协议错误。

## 3. 哪两个地方存在循环？

### 工具调用循环

```text
标签选择 → 工具执行 → 标签选择
```

当标签选择节点认为需要日期计算等外部能力时，先执行工具，再将工具结果带回标签选择节点。

### JSON 重新生成循环

```text
标签选择 → JSON 复核 → 标签选择
```

当模型输出的 JSON 无效时，返回标签选择节点重新生成。

这两个循环都需要关注最大次数、节点超时和总成本。旧版 Graph 没有定义业务级循环预算，只依赖框架的递归限制，生产环境不够明确。

## 4. 最终有哪些结束路径？

存在三个直接连接到 `END` 的节点：

1. `格式化JSON`：成功生成可执行的圈人结果。
2. `提醒无法实现`：标签或能力不足，需求无法完整实现。
3. `非明确圈人意图结束`：模糊需求或非圈人问题。

其中“部分实现”仍会走格式化 JSON；只有 `label_select_output_type == 2`，即完全无法实现时，才进入提醒节点。

## 5. 三个字段分别属于什么阶段？

### `customer_name`

请求输入/运行上下文。它决定读取哪个客户的标签数据。生产系统中更适合改成由认证上下文产生的 `tenant_id`，而不是让客户端任意提交客户名称。

### `session_id`

请求输入/会话上下文。它用于关联多轮对话和历史记忆，不是业务输出。

### `interface_json`

最终业务输出。它是 Agent 生成并格式化后的 QuickAudience 圈人条件。

## 第一遍阅读后最值得继续理解的内容

### A. State 是如何增量更新的

重点观察：初始 State 只有少数字段，每个节点只返回自己新增或修改的字段，LangGraph 将结果合并进共享 State。

建议手动画一张表：

| 节点 | 读取字段 | 写入字段 |
|---|---|---|
| 意图识别 | `user_query` | `intention_answer` |
| Query 改写 | 用户输入、历史 | `original_query`、`rewritten_query` |
| 维度拆解 | 改写 Query、业务知识 | `dimensions`、`dimension_values` |
| 标签召回 | 维度、客户 | `qa_label_metadata` |
| 标签选择 | Query、标签、知识、工具结果 | 标签选择结果 |
| 格式化 JSON | 标签选择结果 | `interface_json` |

### B. Graph 决定流程，Node 决定业务

`graph.py` 主要回答“下一步执行什么”，不会告诉你节点内部究竟如何调用模型、检索数据或构建 DSL。

读完 Graph 后，优先阅读：

1. `nodes/route/agent_route_node.py`：路由值怎样产生。
2. `nodes/operation/dimension_extraction_node.py`：模型怎样产生结构化中间结果。
3. `nodes/operation/label_retrieval_node.py`：如何从维度召回标签。
4. `nodes/llm/agent_llm_node.py`：模型如何选择标签和触发工具。
5. `nodes/operation/agent_operation_node.py`：如何校验并构建最终 JSON。

### C. Graph State 与会话记忆不是一回事

- Graph State：一次 Agent Run 内各节点共享的临时状态。
- Session Memory：跨多次请求保存的历史信息。

当前项目是在运行前从 Qdrant/DashVector 读取历史并放进 State，运行完成后再将结果写回记忆库。

### D. 框架成功不等于业务成功

Graph 能顺利运行到 `END`，只说明流程结束，不代表圈人结果正确。还需要验证：

- 标签是否真实存在。
- 运算符是否适合标签类型。
- 条件组表达式是否引用完整。
- 多轮修改有没有错误继承历史条件。
- 最终 DSL 是否能被 QuickAudience 接口接受。

### E. 固定 Graph 与 Plan-Execute 的区别

当前 `master` 把步骤写死在边中，适合稳定、确定的业务流程。`yili_audience_copilot` 把可执行能力注册为 Executor，由 Planner 决定执行顺序，并通过 Should-Replan 动态调整。

先掌握固定 Graph，再学习 Plan-Execute，会更容易理解为什么线上版本需要 Planner。

## 建议完成的小练习

先不接真实模型，为下面三种输入手写 State 变化：

1. `帮我圈选上海的30岁以上女性。`
2. `帮我圈一些高价值客户。`
3. `今天天气怎么样？`

对每条输入写出：经过哪些节点、哪些节点不会执行、最终从哪个节点进入 `END`。
