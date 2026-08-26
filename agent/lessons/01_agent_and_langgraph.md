# 第 1 课：Agent 与 LangGraph

## 本课目标

- 理解 Agent 与普通 LLM 对话的区别。
- 知道 LangChain 和 LangGraph 在 `es-ai` 中分别负责什么。
- 能够说出圈人 Agent 的输入、状态、决策和输出。

## 1. 什么是业务 Agent

一次普通 LLM 调用通常是：

```text
输入 Prompt → 模型生成文本 → 返回文本
```

业务 Agent 在模型调用之外，还包含状态、流程决策、外部工具和结果校验：

```text
用户输入
→ 读取状态和业务数据
→ 决定下一步
→ 调用模型或工具
→ 校验结果
→ 更新状态
→ 继续执行或结束
```

`es-ai` 的目标不是生成一段看起来合理的回答，而是生成可以被 QuickAudience 执行的圈人条件。因此，最终结构的正确性比语言表达更重要。

## 2. LangChain 与 LangGraph

在 `es-ai` 中：

- LangChain 提供模型封装、消息对象和回调等组件。
- LangGraph 使用 State、Node、Edge 和 Router 编排完整流程。
- OpenAI Python SDK 也被直接用于调用兼容 OpenAI 协议的模型。
- FastAPI 和 SSE 用于把 Agent 作为服务提供给前端。

可以先这样记：

```text
LangChain：怎么调用模型和组织模型能力
LangGraph：多个能力按照什么流程运行
```

## 3. 在 master 中观察 LangGraph

重点文件：

```text
/Users/sumengzhang/Desktop/projects/es-ai/Audience_Copilot/agent/graph.py
```

阅读时寻找以下内容：

- `AgentState`：整个流程共享的数据。
- `StateGraph(AgentState)`：创建工作流。
- `add_node`：注册节点。
- `add_edge`：连接固定路径。
- `add_conditional_edges`：根据状态选择路径。
- `compile()`：编译成可执行 Graph。
- `invoke(initial_state)`：从初始状态运行工作流。

## 4. 第一次源码阅读任务

打开 `graph.py`，完成下面的问题：

1. 工作流的入口节点是什么？
2. 意图识别后有几条分支？
3. 哪两个地方存在循环？
4. 最终有哪些结束路径？
5. `customer_name`、`session_id` 和 `interface_json` 分别属于输入、过程还是输出？

将答案写入：

```text
agent/notes/01_agent_and_langgraph_review.md
```

## 5. 动手练习

先不要调用真实模型。尝试用三个普通 Python 函数模拟：

```text
识别意图 → 提取年龄/性别 → 生成圈人 JSON
```

要求：

- 所有节点通过同一个 State 字典传递数据。
- 非圈人输入直接结束。
- 缺少必需字段时抛出明确异常，不能返回空结果冒充成功。
- 至少准备三个测试输入：正常圈人、非圈人、字段缺失。

练习代码保存到：

```text
agent/exercises/01_minimal_audience_graph/
```

## 复习检查

如果不看资料也能回答下面三个问题，本课就算完成：

1. 为什么圈人 Agent 不能只依赖一次 LLM 调用？
2. State、Node、Edge 分别是什么？
3. LangChain 和 LangGraph 的职责有什么区别？
