# T220: Garage WebEntry Streaming And Live Updates

- Task ID: `T220`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为 `WebEntry` 增加 streaming 与 live session updates，使浏览器入口在不复制 runtime 的前提下看到实时执行、状态变更与最小交互反馈。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T160-garage-local-first-web-control-plane.md`
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`

## 1. 任务目标

这一篇解决的是：

- WebEntry 如何实时看到 session 与 execution 更新
- 浏览器如何消费共享 runtime 的 live events
- streaming 如何保持 local-first 与 one-runtime 语义

## 2. 输入设计文档

- WebEntry 的 local-first control plane 边界
- SessionApi 作为入口请求面
- execution layer 的统一事件语义

## 3. 本文范围

- live session updates
- execution streaming events 的最小暴露方式
- browser reconnect、resume 与最小状态同步
- 与 workspace / evidence 写入的时序关系

## 4. 非目标

- 不在这里设计完整前端状态管理框架
- 不提前引入重型远程消息总线
- 不让浏览器直接订阅 execution internals 而绕过共享 seam

## 5. 交付物

- 一条 WebEntry 可消费的实时事件流
- 一组 session / execution live update 语义
- 一套 reconnect / resume 的最小规则

## 6. 实施任务拆解

### 6.1 冻结 live update 语义

- 明确哪些 session、execution、governance 事件需要实时暴露。
- 明确事件流与 evidence materialization 的关系。

### 6.2 接通共享 runtime seam

- 保证 WebEntry 通过共享入口与 execution event 语义获取更新。
- 避免浏览器直接绕过 `SessionApi` / runtime surface。

### 6.3 补齐 reconnect / resume

- 明确断开重连、浏览器刷新与 session 恢复时如何继续同步。
- 保证 local-first 场景下仍有最小一致性体验。

### 6.4 做最小验证闭环

- 验证 WebEntry 能看到 live session updates。
- 验证 streaming 不会制造第二套 runtime 状态。

## 7. 依赖与并行建议

- 依赖 `16`、`17`
- 应先于 `28`、`29`

## 8. 验收与验证

- WebEntry 已有 streaming 与 live updates 切片
- 浏览器仍复用共享 runtime 主链
- reconnect / resume 语义已可验证

## 9. 完成后进入哪一篇

- `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md`
- `docs/tasks/T222-garage-webentry-governance-and-review-surfaces.md`
