# F163: Execution Trace

- Feature ID: `F163`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 execution trace 的稳定语义。

## 1. 这份文档回答什么

execution trace 应该记录什么、怎样被不同入口读取，以及它如何与 evidence 和 observability 对接。

## 2. owner question

trace 的最小事件语义和 readback 语义由谁统一定义，避免每个入口和每个 provider 自己发明一套运行记录。

## 3. 稳定语义

- trace is a normalized execution record
- trace is readable across entries
- trace supports evidence, diagnostics, and later observability

## 4. 最小事件集合

- started
- partial output streamed
- tool call requested
- tool result returned
- completed
- interrupted
- failed
- blocked

## 5. readback 语义

trace 至少应可按下面维度回读：

- session
- execution request
- node / role context
- provider invocation
- related tool calls

## 6. 边界规则

- trace 不是 provider 私有原始日志
- trace 不是 evidence 本身，但必须能稳定进入 evidence
- trace 不应依赖某个入口的展示方式才成立

## 7. 非目标

- 不做分布式 tracing 平台
- 不把 trace 扩成一切内部状态的黑箱 dump

## 8. Acceptance

- 不同入口和 provider 的执行路径都能归一化到同一组 trace 事件
- trace 可以稳定回指到 session、request、tool call 和 outcome
- 后续 evidence 和 observability 可以共享这条 trace 主线
