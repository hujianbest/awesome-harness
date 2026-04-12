# D22: Host Bridge Product Design

- Design ID: `D22`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `HostBridgeEntry` 作为 capability injection 层时的产品体验模型。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/110-host-bridge-entry.md`
  - `docs/features/F100-agent-teams-product-surface.md`
  - `docs/features/F110-runtime-topology-and-entry-bootstrap.md`

## 1. owner question

当 `Garage` 把能力注入 `Claude`、`OpenCode`、`Cursor` 等工具时，用户应如何感知这种关系。

## 2. 设计判断

- `HostBridge` 不是独立产品主体
- 用户使用的是现有工具，但消费的是 `Garage Team` 的能力
- 宿主不应伪装成 `Garage` 的真相源

## 3. 核心体验

- host context in
- Garage capability out
- shared team/session identity
- governance and review visibility

## 4. 不负责什么

- 不定义宿主协议
- 不定义宿主自己的产品交互体系
