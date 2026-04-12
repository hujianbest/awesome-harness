# F133: Evidence Surface

- Feature ID: `F133`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 evidence surface 的稳定语义。

## 1. 这份文档回答什么

什么东西应该进入 evidence，evidence 在系统里承担什么作用，以及它和 session / memory / archive 的边界在哪里。

## 2. owner question

谁负责写 evidence，什么情况下必须写，什么情况下不能把别的对象误当成 evidence。

## 3. 稳定语义

- evidence records what happened and why
- evidence supports review, traceability, and growth observation
- evidence must remain distinct from memory and session

## 4. 典型 evidence 类型

- governance decision evidence
- execution trace evidence
- review / approval evidence
- bridge acceptance / rework evidence
- verification and validation evidence

## 5. 最小字段语义

每条 evidence 至少应能回指：

- session
- node or team action
- related artifacts
- outcome / verdict
- source pointer

## 6. 边界规则

- evidence 不是长期 memory
- evidence 不是当前 session 状态桶
- evidence 可以成为 growth 观察面，但不直接等于 growth 结果

## 7. 非目标

- 不把所有日志都升格成 evidence
- 不把 evidence 变成新的黑箱事件仓
- 不让 evidence 直接取代 archive / memory / skill

## 8. Acceptance

- 关键执行、治理、review、bridge 行为都能被物化成 evidence
- evidence 可以被后续 traceability 和 growth 主线稳定消费
- evidence 与 session / memory / archive 的边界保持清楚
