# T211: Garage Host Adapter Claude

- Task ID: `T211`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 `Claude` 落成具体 `HostBridgeEntry` adapter，在复用通用宿主桥与共享 authority 的前提下接入 `Garage` runtime。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T150-garage-host-bridge-entry.md`
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F010-shared-contracts.md`

## 1. 任务目标

把通用宿主桥落实到：

- `Claude`

并证明：

- `Claude` 集成不是另一套私有 agent runtime
- `Claude` 通过统一 `SessionApi` 与 authority 主线挂接 `Garage`

## 2. 输入设计文档

- 通用 `HostBridgeEntry` 边界
- `HostAdapterContract` 宿主交互语义
- `RuntimeProfile` authority 与 host hint 分层

## 3. 本文范围

- `Claude` adapter 骨架
- 宿主上下文、消息动作与 `SessionApi` 的最小映射
- workspace / session 绑定与恢复
- 错误、中断、能力限制的最小语义

## 4. 非目标

- 不在这里绑定某个 Claude 发行渠道细节
- 不把 `Claude` 适配变成 provider authority 层
- 不抢先设计所有 Claude UX 细节

## 5. 交付物

- 一套 `Claude` adapter 骨架
- 一组最小动作映射
- 一套 Claude-specific guardrails

## 6. 实施任务拆解

### 6.1 识别 `Claude` 宿主上下文

- 明确 `Claude` 能带来哪些上下文与动作。
- 明确哪些上下文应该进入共享 runtime，哪些只留在宿主边缘。

### 6.2 接通共享 `SessionApi`

- 创建、恢复、提交步骤与审批请求统一进入 `SessionApi`。
- 保证 `Claude` 不直接操作 execution internals。

### 6.3 收紧 authority 与 hint 边界

- 明确 `Claude` hint 只是提示，不是 authority。
- 保证 provider / model 决策继续来自 `RuntimeProfile`。

### 6.4 做最小验证闭环

- 验证 Claude 集成不复制 runtime。
- 验证 session、workspace 与恢复路径稳定。

## 7. 依赖与并行建议

- 依赖 `15`、`17`
- 可与 `T210`、`T212` 并行

## 8. 验收与验证

- `Claude` 已有可执行的宿主 adapter 切片
- `Claude` 复用共享 runtime 主链
- `Claude` 不越权改写 authority

## 9. 完成后进入哪一篇

- 进入 `Claude` 更细的 integration slices，若后续确有需要
