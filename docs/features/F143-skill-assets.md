# F143: Skill Assets

- Feature ID: `F143`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 skill 作为团队可复用资产的稳定语义。

## 1. 这份文档回答什么

什么才算 `Garage Team` 的 skill asset，它和 memory、prompt fragment、一次性经验的边界如何成立。

## 2. owner question

哪些可复用能力应当被视为 skill，哪些还只是临时上下文或未沉淀方法。

## 3. 稳定语义

- skill is a reusable team asset
- skill is not a one-off prompt fragment
- skill evolves under continuity and governance constraints

## 4. 最小语义边界

- skill 代表可复用的方法、流程或能力资产
- skill 可以被不同 session / team actions 回读
- skill 与 raw prompt text 不等价

## 5. 边界规则

- skill 进入长期资产前应有 continuity / governance 路径
- skill 不直接等于 memory
- skill 可以与 packs 协作，但不能反过来定义 core truth

## 6. 非目标

- 不把任何提示片段都升格成 skill
- 不让未经治理的局部 workaround 直接变成 skill
- 不把 skill 设计成宿主私有集成脚手架

## 7. Acceptance

- skill 的长期资产语义清楚
- skill 与 memory / prompt fragment 的边界清楚
- 下游 design 可据此定义 skill 生命周期而不必补脑
