# F122: Session Lifecycle

- Feature ID: `F122`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage Team` 工作主线的 session lifecycle 稳定语义。

## 1. 这份文档回答什么

session 作为团队工作主线，至少有哪些状态、动作和转换约束。

## 2. owner question

团队工作何时算 create、active、pause、resume、closeout，以及这些转换由谁统一定义。

## 3. 稳定语义

- session is the team-work boundary
- lifecycle governs create / active / pause / resume / closeout paths
- session is not a generic history bucket

## 4. 最小动作集

- create
- resume
- attach
- pause
- closeout
- archive-ready progression

## 5. 边界规则

- session lifecycle 语义必须对所有入口一致
- lifecycle 变化需要能被 governance 和 evidence 看见
- 当前 session 边界不能被长期 continuity 对象替代

## 6. 非目标

- 不把 session 设计成所有历史的统一桶
- 不允许入口自己发明不同的 session 状态机

## 7. Acceptance

- 关键 lifecycle 动作有统一语义
- 生命周期变化可被 trace、evidence、governance 共同消费
- 不同入口不会对同一 session 得出不同状态解释
