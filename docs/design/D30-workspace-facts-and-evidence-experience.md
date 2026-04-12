# D30: Workspace Facts And Evidence Experience

- Design ID: `D30`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义用户如何感知 workspace facts、artifacts、evidence 和 authority surfaces。
- 关联文档:
  - `docs/architecture/20-workspace-and-artifact-routing-layer.md`
  - `docs/features/F130-governance-and-workspace-truth.md`

## 1. owner question

用户如何理解什么是当前工作的真实结果、真实证据和真实状态。

## 2. 设计判断

- workspace facts 必须可见、可理解
- evidence 必须可解释，不应退化成隐藏 side-effect
- authority surface 必须让用户知道什么是当前有效结果

## 3. 产品层要求

- artifact visibility
- evidence visibility
- current authority visibility
- archive / history visibility

## 4. 不负责什么

- 不定义持久化实现
- 不定义 schema 细节
