# F144: Growth Proposal And Promotion

- Feature ID: `F144`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `GrowthProposal` 和 promotion 主线的稳定语义。

## 1. 这份文档回答什么

从 evidence 观察到长期更新之间，为什么必须经过 `GrowthProposal`，以及 promotion 的主链如何成立。

## 2. owner question

谁定义 proposal 的存在意义，哪些 promotion 可以发生，哪些必须被阻断或延后。

## 3. 稳定语义

- growth becomes proposal before update
- proposal is the governance object for promotion
- promotion can target memory, skill, or runtime update

## 4. 最小生命周期

- observation
- evidence baseline
- proposal creation
- review / approval / rejection
- accepted promotion target

## 5. promotion target

- memory
- skill
- runtime update

## 6. 边界规则

- proposal 先于 update
- proposal 不等于 evidence 本身
- promotion 不能绕过治理

## 7. 非目标

- 不做无 proposal 的直接自动提升
- 不让 promotion 变成宿主或 pack 的私有 shortcut

## 8. Acceptance

- `GrowthProposal` 的存在意义和生命周期清楚
- promotion target 与治理关系清楚
- 下游 growth design 不需要再猜 proposal 是否是一等对象
