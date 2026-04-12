# F123: Handoff And Review Boundaries

- Feature ID: `F123`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 handoff、review 与团队协作边界的稳定语义。

## 1. 这份文档回答什么

团队内部 handoff 与 review 应该在什么边界上发生，哪些动作必须显式可见。

## 2. owner question

team-level handoff / review 的 owner 语义是什么，以及它与 cross-pack bridge 的关系如何区分。

## 3. 稳定语义

- handoff is explicit
- review is a first-class team action
- boundary transitions must remain visible to governance and evidence

## 4. 和 cross-pack bridge 的区别

- `F123` 负责 team runtime 内部的协作边界
- `F154` 负责跨 pack 的显式 bridge seam
- 二者都要求显式 handoff，但 cross-pack bridge 额外要求 pack 间 artifact/evidence/acceptance 协议

## 5. 最小观察面

- source role / node
- target role / node
- handoff scope
- review verdict or pending state
- related artifacts / evidence

## 6. 非目标

- 不把 handoff 退化成聊天上下文自然延续
- 不把 review 退化成可选附属动作

## 7. Acceptance

- team 内 handoff 和 review 边界可被显式记录
- `F123` 与 `F154` 的 owner 范围不再混写
- governance 与 evidence 可以稳定看到这些边界转换
