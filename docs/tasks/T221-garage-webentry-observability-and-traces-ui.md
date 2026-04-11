# T221: Garage WebEntry Observability And Traces UI

- Task ID: `T221`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为 `WebEntry` 增加 runs、traces、错误与 health 的 observability UI，使浏览器入口能够消费共享 diagnostics 与 trace surface，而不是另造一套 web-only 观测系统。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T160-garage-local-first-web-control-plane.md`
  - `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
  - `docs/tasks/T201-garage-execution-trace-and-evidence-ops-surface.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`

## 1. 任务目标

这一篇解决的是：

- WebEntry 如何查看 runs、traces、errors 与 health
- 浏览器如何消费共享 diagnostics 与 trace surface
- observability UI 如何保持 local-first 与 one-runtime 约束

## 2. 输入设计文档

- WebEntry 的 local-first control plane
- runtime ops baseline 与 diagnostics 语义
- execution trace / evidence ops surface

## 3. 本文范围

- runs / traces / errors / health 的最小浏览 UI
- diagnostics 与 trace 的 readback 语义
- local operator 视角下的最小观察面
- redaction、摘要与 operator-safe 显示规则

## 4. 非目标

- 不在这里设计完整 observability suite
- 不提前实现分布式 tracing dashboard
- 不让 WebEntry 自己定义一套独立日志协议

## 5. 交付物

- 一套 WebEntry observability UI 最小骨架
- 一组浏览 diagnostics 与 traces 的稳定 readback 路径
- 一套 redaction-safe 的 UI 展示规则

## 6. 实施任务拆解

### 6.1 冻结观察对象

- 明确 WebEntry 应该暴露哪些 runs、traces、errors、health 对象。
- 明确它们与 shared diagnostics / trace surface 的对应关系。

### 6.2 接通共享 readback 语义

- 复用 runtime ops 与 trace surface 的 readback 方式。
- 保证 WebEntry 不生成私有 observability 数据面。

### 6.3 收紧展示与 redaction 规则

- 明确哪些字段全文可见，哪些只显示摘要或引用。
- 保持 secrets / authority 相关信息在 UI 中仍然安全。

### 6.4 做最小验证闭环

- 验证 WebEntry 能稳定展示 runs、traces 与 errors。
- 验证 UI 消费的是共享 observability 数据，而不是第二套状态。

## 7. 依赖与并行建议

- 依赖 `22`、`23`、`27`
- 应先于 `30`

## 8. 验收与验证

- WebEntry 已有 observability 与 traces UI 切片
- 浏览器观察面复用了共享 diagnostics / trace 主线
- redaction 与 operator-safe 规则保持成立

## 9. 完成后进入哪一篇

- `docs/tasks/T230-garage-runtime-supervisor-and-multi-workspace-daemon.md`
