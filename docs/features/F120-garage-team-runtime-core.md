# F120: Garage Team Runtime Core

- Feature ID: `F120`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage Team runtime` 的核心对象与团队协作主链，包括 records、session、handoff 与 registry。
- 关联文档:
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/11-runtime-coordination-layer.md`
  - `docs/architecture/102-session-and-session-api.md`

## 1. 这份文档回答什么

支撑 `Garage Team` 工作环境的稳定 runtime core 能力是什么。

## 2. 稳定 capability cut

- neutral runtime records
- `SessionApi`
- `Session`
- handoff and review boundaries
- registry-backed capability discovery

## 3. 不负责什么

- 不定义 pack-specific 扩展语义
- 不定义 provider authority placement
