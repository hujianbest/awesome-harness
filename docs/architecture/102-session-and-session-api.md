# 102: Session And Session API

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 `SessionApi` 与 `Session` 子系统的边界。
- 关联文档:
  - `docs/architecture/11-runtime-coordination-layer.md`

## 1. owner question

所有入口如何进入同一个 session-bound runtime，而不是分别直连内部对象。

## 2. 关键判断

- `SessionApi` is the entry-facing seam
- `Session` is the team-work boundary
- create / resume / attach / submitStep all pass through the same path
- session is not a generic history bucket
