# T210: Garage Host Adapter Cursor

- Task ID: `T210`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 `Cursor` 落成具体 `HostBridgeEntry` adapter，在不复制 runtime 的前提下复用通用宿主桥、共享 authority 与统一 `SessionApi` 主链。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T150-garage-host-bridge-entry.md`
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F010-shared-contracts.md`

## 1. 任务目标

把通用 `HostBridgeEntry` 落到一个具体宿主：

- `Cursor`

并证明：

- `Cursor` 集成复用同一个 `Bootstrap -> SessionApi -> Session` 主链
- `Cursor` 不会各自维护私有 runtime、provider authority 或 execution 逻辑

## 2. 输入设计文档

- 通用 `HostBridgeEntry` 边界
- `RuntimeProfile` authority 与 host hint 边界
- `HostAdapterContract` 的最小宿主交互语义

## 3. 本文范围

- `Cursor` adapter 骨架
- `Cursor` 上下文到 `SessionApi` 的动作映射
- `Cursor` 能力提示、限制与 workspace 绑定
- `Cursor` 错误恢复与最小 UX 约束

## 4. 非目标

- 不在这里替 `Cursor` 设计完整产品体验
- 不把 `Cursor` 适配写成所有宿主的公共逻辑
- 不让 `Cursor` 直接决定 provider / model authority

## 5. 交付物

- 一套 `Cursor` 宿主 adapter 骨架
- 一组 `Cursor` 到 `SessionApi` 的最小映射
- 一套 `Cursor` integration guardrails

## 6. 实施任务拆解

### 6.1 识别 `Cursor` 集成边界

- 明确 `Cursor` 能提供哪些上下文、交互与能力提示。
- 明确哪些上下文应该进入 `SessionApi`，哪些只保留在宿主壳层。

### 6.2 接通统一主链

- create / resume / submitStep / approval 等动作统一映射到 `SessionApi`。
- 保证 `Cursor` 不直接触碰 `Session` / `ExecutionLayer`。

### 6.3 收紧 authority 与能力提示

- 明确 `Cursor` hint 的允许范围。
- 保证 authority 仍由 `RuntimeProfile` 与 runtime 配置链决定。

### 6.4 做最小验证闭环

- 验证 `Cursor` 集成不会制造私有 runtime。
- 验证 workspace、session 与错误恢复路径一致。

## 7. 依赖与并行建议

- 依赖 `15`、`17`
- 可与 `T211`、`T212` 并行

## 8. 验收与验证

- `Cursor` 已有可执行的宿主 adapter 切片
- `Cursor` 复用共享 runtime 主链
- `Cursor` 不抢 authority

## 9. 完成后进入哪一篇

- 进入 `Cursor` 更细的 integration slices，若后续确有需要
