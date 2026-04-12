# 108: CLI Entry

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 `CLIEntry` 作为独立工作环境入口的子系统级架构。
- 关联文档:
  - `docs/architecture/10-entry-and-host-injection-layer.md`

## 1. owner question

CLI 如何作为独立工作环境入口接入同一个 Garage Team runtime。

## 2. 关键判断

- CLI is a first-class product surface
- CLI owns UX, not runtime truth
- CLI uses shared bootstrap and SessionApi
