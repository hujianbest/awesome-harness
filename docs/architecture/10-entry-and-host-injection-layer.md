# 10: Entry And Host Injection Layer

- Architecture Level: `L1`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 回答 `CLI / Web / HostBridge` 三类入口怎样共享产品真相，以及宿主集成如何作为能力注入层存在。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/106-cli-entry.md`
  - `docs/architecture/107-web-entry.md`
  - `docs/architecture/108-host-bridge-entry.md`

## 1. owner question

`Garage` 的独立工作环境和宿主注入层之间，边界应该怎么切。

## 2. 三类入口

- `CLIEntry`：独立工作环境的命令入口
- `WebEntry`：独立工作环境的图形入口
- `HostBridgeEntry`：把 Garage 的 agents、skills 和长期能力注入现有工具

## 3. 关键判断

- `CLI` 与 `Web` 是独立产品入口
- `HostBridge` 是 capability injection，不是新的系统真相
- 所有入口都必须走同一条 `Bootstrap -> SessionApi -> Session` 主链

## 4. 不可越界

- 入口可以有不同 UX，但不能拥有私有 runtime
- 宿主可以提供 hint，但不能成为 authority
- 入口不能直接改写 pack truth、workspace facts 或 growth truth
