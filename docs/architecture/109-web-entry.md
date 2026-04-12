# 109: Web Entry

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 `WebEntry` 作为 local-first 工作环境入口的子系统级架构。
- 关联文档:
  - `docs/architecture/10-entry-and-host-injection-layer.md`

## 1. owner question

Web 如何作为独立工作环境存在，同时不复制第二套 runtime。

## 2. 关键判断

- Web is a first-class product surface
- Web remains local-first by default
- Web uses shared SessionApi and shared execution semantics
