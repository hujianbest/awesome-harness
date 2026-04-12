# F150: Pack Platform And Collaboration

- Feature ID: `F150`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 packs、contracts、registry 与 cross-pack collaboration 的稳定 capability cut。
- 关联文档:
  - `docs/architecture/40-pack-platform-and-extension-layer.md`
  - `docs/architecture/41-cross-pack-bridge-layer.md`
  - `docs/architecture/107-pack-runtime-binding.md`
  - `docs/architecture/111-cross-pack-bridge-protocol.md`

## 1. 这份文档回答什么

Garage Team 如何持续扩展新能力面，以及不同能力面如何显式协作。

## 2. 稳定 capability cut

- shared contracts
- contract schemas
- pack platform
- reference packs
- cross-pack bridge

## 3. 不负责什么

- 不让 packs 拥有 provider authority
- 不把 bridge 升格成 privileged core contract
