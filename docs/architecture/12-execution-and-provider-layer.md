# 12: Execution And Provider Layer

- Architecture Level: `L1`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 回答 provider / tool execution、execution trace 与 authority placement 在整个系统里如何分层。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/103-execution-runtime.md`

## 1. owner question

谁负责执行，谁负责决定是否允许执行，以及 provider authority 放在哪里。

## 2. 核心判断

- execution 负责“怎么做”
- governance 负责“能不能做”
- provider differences stay below core
- provider authority lives in runtime configuration, not in packs or hosts

## 3. 入口关系

- `CLIEntry`、`WebEntry`、`HostBridgeEntry` 都只能通过共享 runtime seam 触发 execution
- 任何入口都不能直接拥有私有 provider invocation 逻辑

## 4. 产物

- tool calls
- provider responses
- execution trace
- evidence materialization
