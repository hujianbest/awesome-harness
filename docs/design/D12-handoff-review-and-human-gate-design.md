# D12: Handoff Review And Human Gate Design

- Design ID: `D12`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 handoff、review、approval 与 human gate 在 `Garage Team` 工作环境中的体验模型。
- 关联文档:
  - `docs/VISION.md`
  - `docs/architecture/30-governance-and-policy-layer.md`
  - `docs/features/F130-governance-and-workspace-truth.md`

## 1. owner question

用户如何感知团队交接、复查和审批，而不是被隐藏在黑箱流程里。

## 2. 设计判断

- handoff 必须可见
- review 必须可见
- approval 必须可见
- human gate 必须是产品层的一等体验，而不是异常分支

## 3. 产品层要求

- 谁把 baton 交给了谁
- 为什么需要 review
- 为什么被卡住
- 需要谁确认
- 确认后会推进到哪一步

## 4. 不负责什么

- 不定义具体 gate runtime 规则
- 不定义 archive / lineage 持久化机制
