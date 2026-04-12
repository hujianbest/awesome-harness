# D11: Multi-Entry Parity And Host Injection Design

- Design ID: `D11`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `CLI / Web / HostBridge` 在产品层的关系、行为一致性和 capability injection 边界。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/10-entry-and-host-injection-layer.md`
  - `docs/features/F100-agent-teams-product-surface.md`
  - `docs/features/F110-runtime-topology-and-entry-bootstrap.md`

## 1. owner question

三个入口怎样共享同一个产品真相，而不是长出三套产品。

## 2. 设计判断

- `CLI` 与 `Web` 是独立产品入口
- `HostBridge` 是能力注入层
- 三类入口都必须能看见同一 team / session / workspace truth
- 宿主集成不应改变 `Garage` 的核心产品关系

## 3. 需要保持一致的东西

- team identity
- session identity
- workspace identity
- governance visibility
- handoff and review semantics

## 4. 不负责什么

- 不定义协议实现
- 不定义具体 provider/tool runtime
