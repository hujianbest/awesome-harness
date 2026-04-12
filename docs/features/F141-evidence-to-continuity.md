# F141: Evidence To Continuity

- Feature ID: `F141`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 evidence 如何成为 continuity 输入的稳定语义。

## 1. 这份文档回答什么

从 evidence 到 continuity 的主链如何成立，以及为什么不能从原始 session 历史直接跳到长期资产。

## 2. owner question

哪一类证据足以进入 continuity 判断，哪些仍然只能停留在瞬时过程层。

## 3. 稳定语义

- evidence precedes continuity decisions
- continuity cannot be inferred from raw session history alone
- evidence is the canonical observation surface for growth

## 4. 输入与输出

输入：

- evidence
- lineage context
- governance-readable outcome

输出：

- continuity candidate
- memory candidate
- skill candidate
- proposal-worthy observation

## 5. 边界规则

- 没有 evidence，就不能进入 continuity promotion 判断
- continuity 输入不能被 host 私有上下文替代
- session 历史可以提供背景，但不能替代 evidence 本身

## 6. 非目标

- 不把所有 evidence 自动升格成 continuity
- 不把 continuity 判断藏在黑箱 heuristic 里

## 7. Acceptance

- continuity 输入有显式 evidence 基线
- continuity 与 raw session history 的边界明确
- 下游 `GrowthProposal` 不需要自己重新定义输入来源
