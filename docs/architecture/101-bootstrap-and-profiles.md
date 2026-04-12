# 101: Bootstrap And Profiles

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 bootstrap、profile selection、runtime home binding 的子系统级架构。
- 关联文档:
  - `docs/architecture/11-runtime-coordination-layer.md`
  - `docs/architecture/10-entry-and-host-injection-layer.md`

## 1. owner question

启动时先解析什么，哪些配置是 authority，哪些只是 hint。

## 2. 关键判断

- bootstrap resolves topology before work starts
- `RuntimeProfile` owns provider/model authority
- host hints cannot override runtime authority
- runtime home and workspace must stay distinct
