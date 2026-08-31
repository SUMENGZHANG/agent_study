# 第 4 课作业评审

## 总体结论

方向基本正确，但当前作业尚未完成，不建议直接进入下一章。

已掌握：

- Graph State 是单次 Graph Run 的状态。
- Session Memory 跨多次 Graph Run 保存。
- 工具执行后会回到标签选择。
- JSON 无效时会回到标签选择重新生成。
- 标签数据库失败不应该返回空标签继续执行。

需要补强：

- 区分节点的输入字段和输出字段。
- 区分模块初始化、请求开始、Graph 开始和 Graph 结束。
- 补全标签选择之后的 State 演进。
- 从源码定位静默兜底，而不是只描述概念。

## 任务一评审：Graph 边界

### Graph 运行前

你的答案：

1. 线程池创建。
2. 查询历史记忆、计算轮次。
3. Snapshot 创建。

其中第 2、3 项正确。线程池在模块加载时创建，不是每个请求调用 Graph 前执行。

更准确的三个请求级操作：

1. FastAPI 解析请求，确定 `session_id`、`user_id`、`customer_name`。
2. 创建 SSE Queue、Snapshot 和 Callback。
3. 查询历史记忆、计算轮次并构造 `initial_state`。

### Graph 结束后

你的三项都有相关性，但时间点需要更精确：

1. 保存记忆到 LlamaIndex/Qdrant：正确。
2. 移除 Snapshot：发生在 SSE Generator 的 `finally`，是整个请求清理阶段。
3. SSE 返回结果：SSE 在 Graph 运行期间已经持续推送；Graph 完成后主要推送最终字段和 `done` 事件。

更准确的答案：

1. 将 Graph 最终字段同步进 Snapshot。
2. 保存本轮 Query、维度、标签结果和 `interface_json` 到记忆库。
3. 推送 `done`，结束请求并移除 Snapshot。

## 任务二评审：完整 State 追踪表

| 节点 | 主要读取字段 | 主要新增/修改字段 | 下一节点如何确定 |
|---|---|---|---|
| 意图识别 | `user_query`、`session_id`、`user_id` | `intention_answer`、`intention_recognition_extra_info`、`collection_name` | Router 根据 `intention_answer` 选择 Query 改写或提前结束 |
| Query 改写 | `user_query`、会话标识、历史记忆、`turn_number` | `original_query`、`rewritten_query`、`turn_number` | 固定 Edge 到业务知识检索 |
| 业务知识检索 | `rewritten_query` 或 `user_query`、`customer_name` | `business_knowledge`、`business_knowledge_raw` | 固定 Edge 到增量调整判断 |
| 增量调整判断 | `original_query/user_query`、会话标识、上一轮结果 | `is_adjustment`、`previous_label_selection`、`adjustment_instruction`、`adjustment_type` | 固定 Edge 到 Query 历史检索 |
| Query 历史检索 | `rewritten_query`、会话标识、`collection_name` | `query_history`、`query_history_scores`、`relative_label_select_result` | 固定 Edge 到维度拆解 |
| 维度拆解 | `rewritten_query/user_query`、`business_knowledge` | `dimensions`、`dimension_values`、`dimension_analysis`、`predict_candidate_label` | 固定 Edge 到相关标签检索 |
| 相关标签检索 | 候选标签、维度取值、客户、阈值 | `qa_label_metadata`、`label_retrieval_stats` | 固定 Edge 到标签选择 |
| 标签选择 | Query、知识、维度、候选标签、历史结果、工具消息 | `label_select_answer` 或 `messages/tool_calls`，以及 `needs_tool` | Router 根据 `needs_tool` 选择工具执行或 JSON 复核 |
| JSON 复核 | `label_select_answer` | `json_valid`、`needs_regenerate`，可能更新答案 | Router 根据 `json_valid` 选择解析结果或回到标签选择 |
| 解析标签选择结果 | `label_select_answer` | `label_select_output_type`、缺失原因、`audience_name` | Router 根据是否完全无法实现选择格式化或提醒 |
| 格式化 JSON | `label_select_answer`、`audience_name` | `interface_json` | 固定 Edge 到 `END` |

主要纠正：

- 意图识别读取的不是 `intention_answer`；它负责生成 `intention_answer`。
- 业务知识节点读取的是 Query，不是“读取知识库”这个 State 字段；知识库是外部资源。
- `total_labels/filtered_labels` 位于 `label_retrieval_stats` 内，不是主要顶层 State 输出。
- 标签选择、JSON 复核、解析和格式化不能留空，它们是最终结果形成的关键链路。

## 任务三评审：两个循环

### 工具循环

- 进入条件：标签选择返回 `needs_tool == True`。
- 路径：标签选择 → 工具执行 → 标签选择。
- 退出条件：再次进入标签选择后不再产生 Tool Call，返回 `needs_tool == False`，随后进入 JSON 复核。

“标签选择节点”本身不是进入条件；真正条件是 State 中的 `needs_tool`。

### JSON 重新生成循环

- 进入条件：JSON 复核返回 `json_valid == False`。
- 路径：JSON 复核 → 标签选择 → JSON 复核。
- 退出条件：`json_valid == True`，进入解析标签选择结果。

## 任务四评审：失败语义

这部分原作业为空，至少应找到三项：

| 文件/函数 | 原始错误 | 当前处理 | 可能造成的业务误判 |
|---|---|---|---|
| `agent_llm_node.node_intention_recognition_non_streaming` | LLM 返回非法 JSON 或非法意图 | 猜第一个字符或强制改成 `"3"` | 明确圈人需求被误报为非圈人 |
| `query_rewriter_node.node_query_rewriter` | 改写模型调用失败 | 使用原始 Query 继续 | “再加上女性”等不完整指令脱离历史执行 |
| `business_knowledge_retrieval_node.node_retrieve_business_knowledge` | Qdrant/Embedding/检索失败 | 返回空知识继续 | 把基础设施故障当成没有相关知识 |
| `label_retrieval_node.node_retrieve_relevant_labels` | MySQL 标签查询失败 | 返回字符串 `[]` 继续 | LLM 在没有真实标签时猜测条件 |
| `agent_llm_node.node_tool_execution` | 未知工具或工具执行失败 | 错误文本作为 Tool Message 返回模型 | 模型可能基于失败文本继续生成结果 |
| `query_history_retrieval_node` | 历史标签 JSON 无法解析 | 跳过该历史记录 | 增量修改丢失已有条件但流程仍显示成功 |

这些情况应根据业务契约返回明确错误码并终止，而不是伪装成“无数据”。

## 任务五评审

### 1. Graph State 与 Session Memory

你的答案正确。

- Graph State：一次 `invoke()` 内的临时共享状态。
- Session Memory：跨多次 `invoke()` 保存的历史数据。

### 2. 为什么 compile 没有自动保存记忆

你的方向正确，但需要补充关键原因：

```python
app = graph.compile()
```

没有传入 Checkpointer。并且本项目的业务记忆不是 LangGraph Checkpoint，而是 API 层在 `invoke()` 完成后显式写入 LlamaIndex/Qdrant。

### 3. 为什么 END 不能证明结果正确

“没有校验结果”不完全准确，因为项目有 JSON 结构复核。

更准确地说：到达 `END` 只证明路由和节点执行结束。JSON 结构合法仍不能证明：

- 标签真实存在。
- 标签属于当前客户。
- 运算符和标签类型匹配。
- 条件语义符合用户要求。
- QuickAudience 下游接口会接受该 DSL。

### 4. 标签数据库失败怎么办

“终止”正确。原因应补充：标签数据库是生成圈人条件的必需数据源。连接失败属于基础设施错误，不等于没有匹配标签；返回空标签继续会诱导模型猜测并制造假成功。

## 修改要求

请回到原 `worksheet.md`：

1. 修正任务一。
2. 独立补全任务二后半部分。
3. 将任务三的条件写成具体 State 判断。
4. 在任务四至少填写三个源码位置。
5. 补完整任务五第 2～4 题的原因。

修改时可以参考本评审，但请用自己的语言重新表达。
