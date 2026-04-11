# T212: Garage Host Adapter OpenCode

- Task ID: `T212`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 `OpenCode` 落成具体 `HostBridgeEntry` adapter，在复用统一宿主桥、共享 authority 与 `SessionApi` 的前提下接入 `Garage` runtime。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T150-garage-host-bridge-entry.md`
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F010-shared-contracts.md`

## 1. 任务目标

把通用宿主桥落实到：

- `OpenCode`

并证明：

- `OpenCode` 集成仍是 `Garage` 的一个宿主壳，而不是另一套 runtime
- `OpenCode` 通过统一 `SessionApi`、authority 与治理主线接入系统

## 2. 输入设计文档

- 通用 `HostBridgeEntry` 边界
- `HostAdapterContract` 最小宿主交互语义
- provider authority 与 host hint 分层

## 3. 本文范围

- `OpenCode` adapter 骨架
- 宿主动作到 `SessionApi` 的最小映射
- workspace / session 恢复语义
- 能力提示、限制与错误恢复边界

## 4. 非目标

- 不在这里实现所有 OpenCode UX
- 不把 OpenCode 适配扩成新的 provider gateway
- 不让 OpenCode 直接持有 runtime authority

## 5. 交付物

- 一套 `OpenCode` adapter 骨架
- 一组最小动作映射
- 一套 OpenCode-specific guardrails

## 6. 实施任务拆解

### 6.1 识别 `OpenCode` 宿主上下文

- 明确 `OpenCode` 能提供的上下文、能力提示与交互动作。
- 区分进入共享 runtime 的输入与留在宿主边缘的输入。

### 6.2 接通共享 `SessionApi`

- create / resume / submitStep / approval 等动作统一映射到 `SessionApi`。
- 保证 `OpenCode` 不直接触碰 `Session` / `ExecutionLayer`。

### 6.3 收紧 authority 边界

- 明确 `OpenCode` 的 hint 与限制语义。
- 保证 provider / model authority 仍然来自 runtime 配置链。

### 6.4 做最小验证闭环

- 验证 OpenCode 集成不复制 runtime。
- 验证 workspace、session 与恢复语义稳定。

## 7. 依赖与并行建议

- 依赖 `15`、`17`
- 可与 `T210`、`T211` 并行

## 8. 验收与验证

- `OpenCode` 已有可执行的宿主 adapter 切片
- `OpenCode` 复用共享 runtime 主链
- `OpenCode` 不越权改写 authority

## 9. 完成后进入哪一篇

- 进入 `OpenCode` 更细的 integration slices，若后续确有需要
