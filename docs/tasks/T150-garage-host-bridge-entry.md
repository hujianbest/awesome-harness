# T150: Garage Host Bridge Entry

- Task ID: `T150`
- 状态: 已完成
- 日期: 2026-04-11
- 定位: 把 `Claude`、`OpenCode`、`Cursor` 一类宿主集成收敛到通用 `HostBridgeEntry` 与薄适配层，使宿主差异留在桥边缘，而不是在每个宿主里各长一套 runtime。
- 当前阶段: 完整架构主线下的第二组独立入口 implementation tracks
- 关联设计文档:
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`
  - `docs/architecture/A120-garage-core-subsystems-architecture.md`
  - `docs/features/F010-shared-contracts.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`

## 1. 任务目标

在 `CLIEntry` 已成为第一条真实入口后，这一篇继续解决：

- 宿主集成如何接进同一个 runtime

它要证明的是：

- `HostBridgeEntry` 是一类通用入口 family，而不是某个宿主的私有特例
- `Claude`、`OpenCode`、`Cursor` 等集成都通过同一条 `Bootstrap -> SessionApi -> Session` 主链挂接
- 宿主只能提供能力提示与交互壳，不能反向拥有 provider authority 或 runtime 主线

## 2. 输入设计文档

这一篇主要承接：

- `HostBridgeEntry` 作为一等入口 family
- `HostAdapterContract` 的最小宿主交互语义
- `SessionApi` 作为 entry-facing session seam
- provider / tool execution 与 host boundary 的分层约束
- `runtime home` 中 `RuntimeProfile` 的 provider authority

## 3. 本文范围

- 通用 `HostBridgeEntry` 入口骨架
- `HostAdapterContract` 到 `SessionApi` 的统一映射
- 宿主能力边界、限制与提示的表达方式
- 宿主本地上下文与 workspace / session 绑定
- 宿主错误、恢复与中断路径

## 4. 非目标

- 不在这里深度定制某一个宿主的专属 UX
- 不把宿主桥直接扩成 provider gateway
- 不让 `Claude`、`OpenCode`、`Cursor` 各自持有私有 runtime services
- 不一次性设计 remote multi-host coordination

## 5. 交付物

- 一个通用 `HostBridgeEntry` 最小入口骨架
- 一组宿主请求到 `SessionApi` 的最小动作映射
- 一套宿主 capability hint 与 runtime authority 的边界约束
- 至少一组可供后续具象宿主复用的薄适配模式
- 给 `16` 与 `17` 复用的宿主桥边界前提

## 6. 实施任务拆解

### 6.1 冻结通用宿主桥形状

- 明确 `HostBridgeEntry` 接受哪些宿主输入与上下文。
- 明确哪些动作必须通过 `HostAdapterContract` 暴露。
- 避免为了某个宿主先发明私有桥协议。

### 6.2 把宿主请求统一送进 `SessionApi`

- create / resume / submitStep / requestApproval / closeout 等动作统一映射到 `SessionApi`。
- 保证宿主不能绕过 `SessionApi` 直接触碰 `Session` 或 `ExecutionLayer`。
- 让宿主桥与 CLI 共用同一条 bootstrap / session 主链。

### 6.3 冻结宿主 capability hint 边界

- 明确宿主可以提交哪些本地能力提示、展示偏好与限制。
- 明确宿主限制能力，不等于宿主重写工具语义。
- 明确宿主不能把 vendor / model 细节直接写成当前 session authority。

### 6.4 做薄适配层，而不是再造 runtime

- 为 `Claude`、`OpenCode`、`Cursor` 预留薄适配模式。
- 保证宿主差异停留在 bridge edge，不扩散到 core、packs 或 execution objects。
- 避免每个宿主自己维护 session 恢复、tool routing 与 provider 解析逻辑。

### 6.5 做最小验证闭环

- 验证宿主桥可以稳定 create / resume 并绑定 workspace。
- 验证 host hint 与 `RuntimeProfile` authority 不冲突。
- 验证新宿主接入时复用的是同一桥语汇，而不是新的 runtime 方言。

## 7. 依赖与并行建议

- 依赖 `12`、`13`、`14`
- 应在 `16` 前完成，避免 web 与宿主桥各自扩张入口语义
- 与具体宿主的 UX 细化可以后置，但通用桥边界必须先稳定

## 8. 验收与验证

完成这篇任务后，应能验证：

- `HostBridgeEntry` 已成为独立但通用的入口切片
- 宿主通过同一条 `GarageLauncher -> SessionApi` 主链进入系统
- 宿主差异不会重新制造私有 runtime
- host 只能给 hint，不能抢 provider / pack authority

## 9. 完成后进入哪一篇

- `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
- `docs/tasks/T210-garage-host-adapter-cursor.md`
- `docs/tasks/T211-garage-host-adapter-claude.md`
- `docs/tasks/T212-garage-host-adapter-opencode.md`
