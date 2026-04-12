# F164: Evidence-Linked Execution Outcomes

- Feature ID: `F164`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 execution outcome 与 evidence 绑定关系的稳定语义。

## 1. 这份文档回答什么

一次 execution 完成后，什么样的 outcome 必须被 evidence-linked，哪些对象之间必须能互相回指。

## 2. owner question

谁负责把 execution 结果从“运行完成”推进到“可追溯、可治理、可成长观察”的状态。

## 3. 稳定语义

- execution outcomes must remain evidence-linked
- outcomes support traceability and growth observation
- execution completion does not bypass governance

## 4. 最小绑定关系

一次 evidence-linked execution outcome 至少应能回指：

- execution request
- execution trace
- session
- related tool results
- materialized evidence record
- lineage link when applicable

## 5. 进入条件

下面这些执行结果必须进入 evidence-linked outcome 主线：

- completed execution
- blocked execution
- failed execution
- interrupted execution

## 6. 边界规则

- “执行完了” 不等于 “可以跳过 evidence”
- execution outcome 可以成为 growth 输入，但不直接等于长期资产
- outcome 绑定关系必须对 CLI / Web / HostBridge 一致成立

## 7. 非目标

- 不把所有 provider 原始响应全文保存成主事实
- 不让 execution outcome 直接绕过 governance 进入 memory / skill

## 8. Acceptance

- 关键 execution outcome 全部有稳定 evidence linkage
- 下游 traceability 和 growth 不需要自己补猜 outcome 来源
- 不同入口不会生成不同的 outcome 绑定逻辑
