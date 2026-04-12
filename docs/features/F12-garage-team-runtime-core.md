# F12: Garage Team Runtime Core

- Feature ID: `F12`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage Team runtime` 的核心对象与团队协作主链，包括 records、session、handoff、review 与 registry。
- 关联文档:
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/11-runtime-coordination-layer.md`
  - `docs/architecture/102-session-and-session-api.md`
  - `docs/features/F121-neutral-runtime-records.md`
  - `docs/features/F122-session-lifecycle.md`
  - `docs/features/F123-handoff-and-review-boundaries.md`
  - `docs/features/F124-registry-backed-capability-discovery.md`

## 1. 这份文档回答什么

支撑 `Garage Team` 工作环境的稳定 runtime core 能力是什么。

## 2. stable capability family

- neutral runtime records
- `SessionApi`
- `Session`
- handoff and review boundaries
- registry-backed capability discovery

`SessionApi` 的规范 owner 在 `F113`，本 family 只把它视为 team runtime core 的一个关键组成部分，而不重复定义它的 entry-facing seam。

## 3. 下游 specs

- `F121`：neutral runtime records
- `F122`：session lifecycle
- `F123`：handoff and review boundaries
- `F124`：registry-backed capability discovery
- `F113`：SessionApi 与 shared entry binding（跨 family 依赖）
