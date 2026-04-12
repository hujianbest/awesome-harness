# F134: Governance Gates, Approval, And Archive

- Feature ID: `F134`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 governance gates、approval 和 archive 的稳定语义。

## 1. 这份文档回答什么

治理如何真正进入工作主线，以及 gate / approval / archive 各自负责什么。

## 2. owner question

哪些动作必须被 gate 约束，哪些结果必须经过 approval，archive 何时才算显式完成。

## 3. 稳定语义

- governance is artifact-first
- gates and approvals constrain work progression
- archive remains a visible governance result, not a hidden side effect

## 4. 最小治理动作

- allow
- block
- needs-review
- needs-approval
- archive-ready / archived progression

## 5. 边界规则

- gate 不是 UI 提示，而是 runtime 约束
- approval 不是聊天口头确认，而是显式治理动作
- archive 不能悄悄变成副作用

## 6. 非目标

- 不把治理完全埋进 prompts
- 不让 archive 取代 evidence 或 continuity

## 7. Acceptance

- 关键团队动作都能被 gate / approval 语义约束
- archive 是可见、可追溯的治理结果
- 不同入口不会各自发明不同的 gate / approval 含义
