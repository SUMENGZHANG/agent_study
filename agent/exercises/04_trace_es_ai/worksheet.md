# 第 4 课答案：追踪 `es-ai master`

## 请求

```text
帮我圈选上海30岁以上的女性用户
```

假设首轮、无需工具、模型输出合法、需求可以实现。

## 任务一：划分边界

### Graph 运行前

1. FastAPI 解析请求，确定 `session_id`、`user_id` 和 `customer_name`。
2. 创建 SSE Queue、Snapshot 和 Callback，用于推送运行过程。
3. 查询历史记忆、计算 `turn_number`，构造传给 `invoke()` 的 `initial_state`。

线程池在模块加载时创建，不是每次 Graph 运行前重新创建。

### Graph 结束后

1. 将最终 State 中的意图、标签选择结果、名称和 `interface_json` 同步到 Snapshot。
2. 将本轮 Query、维度、标签结果和最终 JSON 保存到 LlamaIndex/Qdrant 记忆库。
3. 推送 SSE `done` 事件；请求结束时移除当前 Session 的 Snapshot。

SSE 并非只在 Graph 结束后返回，它在 Graph 运行期间会持续推送节点事件。

## 任务二：State 追踪表

| 节点 | 主要读取字段 | 主要新增/修改字段 | 下一节点如何确定 |
|---|---|---|---|
| 意图识别 | `user_query`、`session_id`、`user_id` | `intention_answer`、`intention_recognition_extra_info`、`collection_name` | Router 根据意图值 `1/2/3` 选择 Query 改写或提前结束 |
| Query 改写 | `user_query`、会话标识、历史记忆、`turn_number` | `original_query`、`rewritten_query`、`turn_number` | 固定 Edge 到业务知识检索 |
| 业务知识检索 | `rewritten_query` 或 `user_query`、`customer_name` | `business_knowledge`、`business_knowledge_raw` | 固定 Edge 到增量调整判断 |
| 增量调整判断 | 当前 Query、会话标识、上一轮标签结果 | `is_adjustment`、`previous_label_selection`、`adjustment_instruction`、`adjustment_type` | 固定 Edge 到 Query 历史检索 |
| Query 历史检索 | `rewritten_query`、会话标识、`collection_name` | `query_history`、`query_history_scores`、`relative_label_select_result` | 固定 Edge 到维度拆解 |
| 维度拆解 | `rewritten_query/user_query`、`business_knowledge` | `dimensions`、`dimension_values`、`dimension_analysis`、`predict_candidate_label` | 固定 Edge 到相关标签检索 |
| 相关标签检索 | 候选标签、维度取值、客户、相似度配置 | `qa_label_metadata`、`label_retrieval_stats` | 固定 Edge 到标签选择 |
| 标签选择 | Query、知识、维度、标签、历史结果、工具消息 | 无工具时写 `label_select_answer`；有工具时写 `messages`、`tool_calls`；同时写 `needs_tool` | Router 根据 `needs_tool` 选择工具执行或 JSON 复核 |
| JSON 复核 | `label_select_answer` | `json_valid`、`needs_regenerate`，可能更新 `label_select_answer` | Router 根据 `json_valid` 选择解析结果或重新生成 |
| 解析标签选择结果 | `label_select_answer` | `label_select_output_type`、`label_select_deficiency_reason`、`audience_name` | Router 根据是否完全无法实现选择格式化或提醒 |
| 格式化 JSON | `label_select_answer`、`audience_name` | `interface_json` | 固定 Edge 到 `END` |

## 任务三：解释两个循环

### 工具循环

- 进入条件：标签选择返回 `needs_tool == True`。
- 循环路径：标签选择 → 工具执行 → 标签选择。
- 退出条件：再次进入标签选择后不再产生 Tool Call，返回 `needs_tool == False`，进入 JSON 复核。

### JSON 重新生成循环

- 进入条件：JSON 复核返回 `json_valid == False`。
- 循环路径：JSON 复核 → 标签选择 → JSON 复核。
- 退出条件：`json_valid == True`，进入解析标签选择结果。

## 任务四：识别失败语义

| 文件/函数 | 原始错误 | 当前处理 | 可能造成的业务误判 |
|---|---|---|---|
| `agent_llm_node.node_intention_recognition_non_streaming` | LLM 返回非法 JSON 或非法意图 | 猜第一个字符或改成 `"3"` | 明确圈人需求被误报为非圈人 |
| `query_rewriter_node.node_query_rewriter` | Query 改写模型失败 | 使用原始 Query 继续 | 增量指令脱离历史，被当成完整需求执行 |
| `business_knowledge_retrieval_node.node_retrieve_business_knowledge` | Qdrant、Embedding 或检索失败 | 返回空知识继续 | 基础设施故障被误认为没有业务知识 |
| `label_retrieval_node.node_retrieve_relevant_labels` | MySQL 标签查询失败 | 返回空标签继续 | LLM 在没有真实标签时猜测圈人条件 |
| `agent_llm_node.node_tool_execution` | 未知工具或执行失败 | 将错误文本作为 Tool Message 返回模型 | 模型可能基于失败结果继续生成 |
| `query_history_retrieval_node` | 历史标签 JSON 解析失败 | 跳过记录 | 增量修改丢失已有条件但流程仍继续 |

正确原则：必需数据或上游调用失败时，应返回明确错误码和 `trace_id`，立即终止 Graph。不能用空字符串、空数组或默认业务结果伪装成功。

## 任务五：概念问答

### 1. Graph State 与 Session Memory 有什么区别？

Graph State 是一次 `invoke()` 内部各节点共享的临时状态，随着 Node 执行不断合并更新。Session Memory 是跨多次 `invoke()` 保存的历史数据，用于多轮对话、Query 改写和增量修改。

### 2. 为什么 `app = graph.compile()` 没有自动保存多轮记忆？

本项目调用 `graph.compile()` 时没有传入 Checkpointer。并且项目所说的业务记忆不是 Graph Checkpoint，而是 API 层在 `invoke()` 完成后显式写入 LlamaIndex/Qdrant 的 Query 和标签结果。

### 3. 为什么 Graph 到达 `END` 不能证明圈人结果正确？

到达 `END` 只证明节点调度和路由已经结束。即使 JSON 结构合法，也不能证明：

- 标签真实存在且属于当前客户。
- 运算符与标签类型匹配。
- 条件语义符合用户原始要求。
- 历史条件没有被错误增加或删除。
- QuickAudience 下游接口能够接受该 DSL。

所以还需要标签校验、DSL 语义校验、下游协议校验和业务评测。

### 4. 标签数据库连接失败时应该怎么办？

应该终止 Graph。标签数据库是生成圈人条件的必需数据源，连接失败属于基础设施错误，不等于没有匹配标签。返回空标签继续会诱导模型猜测不存在的标签，产生假成功。

## 本章结论

```text
HTTP 请求
→ API 构造初始 State
→ LangGraph 调度节点并合并 State
→ 生成 interface_json
→ END
→ API 保存记忆并完成 SSE
```

最重要的认识：

```text
Graph 到达 END ≠ 圈人业务正确
无数据 ≠ 上游调用失败
结构合法 ≠ 语义合法
```
