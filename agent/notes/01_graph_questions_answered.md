# 第一次阅读 `graph.py` 的问题与解答

## 1. 第一步是 Query Rewrite 吗？它是必须的吗？

先纠正一个小点：Graph 的第一个节点是“意图识别”，只有明确圈人意图才进入 Query Rewrite。

```text
意图识别
├── 明确圈人 → Query Rewrite → 后续圈人流程
└── 模糊/非圈人 → 提前结束
```

### Query Rewrite 不是所有 Agent 都必须有

它主要解决多轮对话中的省略和指代。例如：

```text
第一轮：帮我圈选上海30岁以上的女性
第二轮：再加上最近30天购买过商品
```

第二轮单独看并不是完整需求。改写后可以变成：

```text
圈选上海30岁以上女性，并且最近30天购买过商品
```

如果是首轮完整请求，当前项目直接保留原 Query，不调用改写模型。

### 优点

- 将依赖历史的短句补成完整需求。
- 下游节点不必都理解多轮上下文。
- 便于记录、检索和调试“本轮最终有效需求”。
- 降低每个下游 Prompt 都携带完整历史的成本。

### 缺点

- 可能错误添加、删除或改变用户条件。
- 多一次模型调用，增加耗时和 Token 成本。
- 如果只保存改写结果，可能丢失“增加、删除、修改”等操作意图。
- 历史选择不准确时，错误会传播到所有下游节点。

### 常见实现方式

1. **LLM 改写**：当前项目采用的方式。把最近几轮历史和当前 Query 交给模型。
2. **规则改写**：识别“再加上、去掉、改成”等明确操作，适合规则稳定的业务。
3. **结构化状态更新**：不生成新文本，直接对上一轮 `AudienceIntent` 或 DSL 做增删改。执行型业务通常更可靠。
4. **混合方式**：LLM 负责理解意图，确定性代码更新结构化状态。

对于圈人系统，长期更推荐第 4 种。文本改写可用于理解和展示，但最终条件修改应通过结构化操作完成。

当前实现还有一个风险：改写调用失败后会把原始 Query 当作改写成功结果继续执行。这样会把“再加上女性”这种不完整请求传给下游。更合理的处理是返回明确的 `QUERY_REWRITE_FAILED` 并终止本次运行。

## 2. LlamaIndex 是什么？在项目中有什么作用？

LlamaIndex 是帮助 LLM 应用接入外部数据的框架。它提供：

- Document：要存储和检索的数据。
- Embedding 接口：把文本转换成向量。
- Vector Store 适配：对接 Qdrant 等数据库。
- Index/Retriever：建立索引并执行检索。
- Metadata Filter：按用户、会话等元数据过滤。
- 混合检索：组合稠密向量和稀疏关键词检索。

在当前项目中，LlamaIndex 主要负责“会话历史的存储和检索”。它本身不保存数据，而是组织检索流程，底层数据实际存在 Qdrant。

```text
Agent 节点
→ LlamaIndexMemoryManager
→ LlamaIndex 的 Index / VectorStore
→ Qdrant
```

可以先这样理解：

```text
LlamaIndex = 检索应用层/适配层
Qdrant      = 真正保存和查询向量的数据服务
```

## 3. Qdrant 是什么？在项目中有什么作用？

Qdrant 是向量数据库。它能保存：

- 向量：例如 1024 个浮点数表示一段文本的语义。
- Payload：原始 Query、改写 Query、用户 ID、会话 ID、时间等业务字段。
- 稀疏向量：用于 BM25 一类关键词检索。

普通数据库擅长精确查询：

```sql
WHERE session_id = '123'
```

向量数据库还可以查询“语义上最相似的内容”：

```text
“最近买过奶粉的人”
≈ “近30天有奶粉购买行为的用户”
```

当前项目用 Qdrant 保存和检索：

- 会话历史 Query。
- 改写后的 Query。
- 标签选择结果等元数据。
- 业务知识向量。

项目同时使用 `user_id` 和 `session_id` 过滤，避免检索到其他会话的数据。

## 4. Embedding 和 `AliyunEmbedding` 的作用是什么？

Embedding 是把文本转换成一组数字：

```text
“上海女性用户” → [0.12, -0.37, 0.81, ...]
```

语义接近的文本，其向量通常也更接近。程序可以通过余弦相似度寻找相关文本。

`AliyunEmbedding` 是当前项目为 LlamaIndex 编写的适配器：

```text
LlamaIndex 请求生成向量
→ AliyunEmbedding
→ 阿里云 text-embedding-v4
→ 返回 1024 维向量
```

它继承 LlamaIndex 的 `BaseEmbedding`，实现了单文本、批量文本和 Query 的向量生成接口。这样 LlamaIndex 不需要知道底层调用的是阿里云还是其他模型。

这里还要注意一个明显风险：当前代码在 Embedding 调用失败时返回全零向量。全零向量没有真实语义，却会继续参与存储或检索，可能产生错误结果。正确做法是抛出明确异常并终止当前检索。

## 5. `add_conditional_edges` 的类型标注是什么意思？

这段代码主要属于 **Python 类型标注**，不是线程代码：

```python
def add_conditional_edges(
    self,
    source: str,
    path: Callable[..., Hashable | Sequence[Hashable]]
        | Callable[..., Awaitable[Hashable | Sequence[Hashable]]]
        | Runnable[Any, Hashable | Sequence[Hashable]],
    path_map: dict[Hashable, str] | list[str] | None = None,
)
```

### 参数含义

- `self`：当前 `StateGraph` 对象。
- `source: str`：从哪个节点出发。
- `path`：执行完 source 后，用什么函数决定下一条路。
- `path_map`：把路由函数返回值映射成真实节点名。

项目中的调用：

```python
graph.add_conditional_edges(
    "意图识别",
    route_after_intention,
    {
        "1": "Query改写器",
        "2": "非明确圈人意图结束",
        "3": "非明确圈人意图结束",
    },
)
```

执行过程：

```text
意图识别节点执行完成
→ 调用 route_after_intention(state)
→ 假设返回 "1"
→ path_map["1"] 得到 "Query改写器"
→ 执行 Query 改写器
```

### 需要认识的类型

#### `Callable`

表示“可以调用的对象”，最常见就是函数。

```python
Callable[[int, int], int]
```

表示接收两个 `int`、返回一个 `int` 的函数。

`Callable[..., str]` 中的 `...` 表示参数形式不限，返回 `str`。

#### `Hashable`

表示可以作为字典 Key 的值，例如字符串、整数和元组。列表和字典不是 Hashable。

路由结果要拿去查 `path_map`，所以必须能作为 Key。

#### `Sequence[Hashable]`

表示一组有顺序的路由结果，例如列表或元组。LangGraph 允许一次返回多个目标，从而向多个节点分发。

#### `Awaitable[T]`

表示一个稍后才能获得 `T` 的异步结果。通常来自 `async def` 函数。

```python
async def route(state) -> str:
    return "next"
```

调用异步函数不会立刻得到字符串，而是先得到 Awaitable；通过 `await` 才获得最终字符串。

#### `Runnable[Input, Output]`

这是 LangChain 的统一可执行对象接口。普通函数、Prompt、模型和组合链可以被包装成 Runnable。

这里表示：输入类型不限，输出一个路由值或一组路由值。

#### `A | B` 和 `None`

`A | B` 表示参数可以是 A 或 B。

```python
dict[Hashable, str] | list[str] | None
```

表示 `path_map` 可以是字典、字符串列表或者不传。

### 现在需要学线程吗？

理解这段签名暂时不需要线程知识。建议顺序是：

1. 普通函数和函数作为参数。
2. 类型标注与泛型容器。
3. `Callable`、`Hashable`、`Sequence`。
4. `async def`、`await`、`Awaitable`。
5. 最后再学习线程、线程池和 FastAPI 并发。

异步和线程都能处理并发，但原理不同，暂时不要混在一起学习。

## 这些组件之间的关系

```text
用户 Query
→ LangGraph 决定执行哪些节点
→ Query Rewrite 结合会话历史补全需求
→ LlamaIndex 组织历史检索
→ AliyunEmbedding 将文本转为稠密向量
→ Qdrant 保存向量、Payload 并执行相似度检索
→ 检索结果回到 LangGraph State
```

## 下一步练习

### 练习 1：手写条件路由

不使用 LangGraph，实现：

```python
def route(score: int) -> str:
    ...

path_map = {
    "pass": "生成结果",
    "retry": "重新生成",
}
```

根据 score 返回路由值，再通过 `path_map` 找到下一节点。

### 练习 2：体验 Embedding 思想

先不调用真实 Embedding，用关键词集合模拟文本向量，比较两句话的共同词数量。目标不是实现真正向量，而是理解“把文本转换成可比较的数字表示”。

### 练习 3：分析 Query Rewrite

为下面输入分别写出：是否需要改写、期望改写结果、改写错误可能造成什么影响。

1. 首轮：`帮我圈选上海女性。`
2. 上一轮已圈上海女性，本轮：`再加上30岁以上。`
3. 上一轮已圈上海女性，本轮：`重新圈选北京男性。`
