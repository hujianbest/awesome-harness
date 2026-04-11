# T201: Garage Execution Trace And Evidence Ops Surface

- Task ID: `T201`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 execution trace、evidence materialization 与 operator-facing trace surface 收敛成统一观察面，使运行中的执行路径、失败点与留痕结果都可被持续检查。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
  - `docs/tasks/T130-garage-runtime-provider-and-tool-execution.md`
  - `docs/features/F060-artifact-and-evidence-surface.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`
  - `docs/architecture/A120-garage-core-subsystems-architecture.md`

## 1. 任务目标

这一篇解决的是：

- execution trace 如何被 operator 看见
- trace 与 evidence / archive / lineage 如何被统一关联
- 运行失败时如何快速回到对应 session、node、artifact 与证据

## 2. 输入设计文档

这一篇主要承接：

- execution layer 已有统一 trace / event 语义
- artifact / evidence surfaces 已是 workspace-first 真相面
- runtime ops baseline 已有结构化 diagnostics 与 health surface

## 3. 本文范围

- execution trace 的 operator-facing surface
- trace 到 evidence / lineage / artifact 的最小关联方式
- 失败、重试、中断与审批挂点的 trace 观察方式
- local diagnostics 与后续 Web observability 可复用的数据面

## 4. 非目标

- 不做分布式 tracing 平台
- 不把 evidence 变成不可控的大型事件总线
- 不提前设计完整 query language
- 不让 trace surface 直接替代 governance 或 archive 判断

## 5. 交付物

- 一条 execution trace 到 evidence 的可检查链路
- 一组 trace 观察对象与 readback 语义
- 一套失败、中断、tool call 与审批节点的追踪入口
- 给 `T221` 与 operator runbooks 复用的 trace 基线

## 6. 实施任务拆解

### 6.1 冻结 trace readback 语义

- 明确 trace 如何按 session、node、run 或 execution id 被读取。
- 明确 trace 中哪些字段直接映射到 evidence / lineage。
- 保持 readback 语义不依赖某个特定入口。

### 6.2 关联 evidence、artifacts 与 lineage

- 让 trace 可以回指对应 artifact writes、evidence records 与 archive 节点。
- 让 operator 能回答“发生了什么、留下了什么、为什么失败”。
- 避免 trace 和 evidence 再次分桶成两套真相。

### 6.3 补齐失败与中断观察面

- 明确失败、中断、tool call、approval checkpoint 等关键节点如何被看到。
- 明确哪些信息进入 operator surface，哪些只保留摘要。
- 保证 redaction 与安全输出规则继续成立。

### 6.4 接入后续 UI 与 ops 流程

- 让 Web observability 与 traces UI 复用同一 trace surface。
- 让 release smoke 与 runtime ops 复用相同 trace readback 语义。
- 避免每个入口自己发明“查看运行过程”的私有方式。

### 6.5 做最小验证闭环

- 验证一条 execution 可以回指 session、node、artifact 与 evidence。
- 验证失败与中断能够被稳定追踪。
- 验证 trace surface 足以支撑后续 web observability。

## 7. 依赖与并行建议

- 依赖 `13`、`22`
- 应先于 `28`
- 与具体宿主 adapter 实现可并行，但 trace 语义应保持全入口共享

## 8. 验收与验证

完成这篇任务后，应能验证：

- execution trace 已成为可检查、可追溯的运维观察面
- evidence、artifacts 与 lineage 能与 trace 稳定互指
- 失败、中断与审批节点不再是黑箱
- Web observability 与更重 ops 面已有稳定 trace 基线

## 9. 完成后进入哪一篇

- `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md`
