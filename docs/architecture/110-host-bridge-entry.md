# 110: Host Bridge Entry

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 `HostBridgeEntry` 作为 capability injection 层的子系统级架构。
- 关联文档:
  - `docs/architecture/10-entry-and-host-injection-layer.md`

## 1. owner question

已有工具如何注入 Garage 能力，而不抢走 Garage 的系统真相。

## 2. 关键判断

- HostBridge is capability injection, not product authority
- host can provide hints and local context
- host cannot override runtime truth, pack truth, or growth truth
