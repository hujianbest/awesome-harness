# 104: Artifact Routing And Workspace Facts

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 artifact routing、workspace facts 与 authority surface 的子系统级架构。
- 关联文档:
  - `docs/architecture/20-workspace-and-artifact-routing-layer.md`

## 1. owner question

工作结果怎样进入 workspace-first truth，并保持 authority 清晰。

## 2. 关键判断

- artifact routing maps neutral intent to authoritative surfaces
- workspace facts remain readable and durable
- runtime home does not own artifacts or evidence
