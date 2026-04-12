# F142: Memory

- Feature ID: `F142`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 memory 作为长期团队状态的稳定语义。

## 1. 这份文档回答什么

什么才算 `Garage Team` 的 memory，它和 evidence、session、skill 的边界如何成立。

## 2. owner question

哪些长期状态应当进入 memory，哪些仍然只能停留在 evidence、session 或 skill。

## 3. 稳定语义

- memory is long-horizon team state
- memory is not raw evidence or current session context
- memory must stay reviewable and scoped

## 4. 最小语义边界

- memory 保存长期可回读的团队状态
- memory 可以被未来 session 消费
- memory 不直接等于某次执行过程留下的原始痕迹

## 5. 边界规则

- evidence 先于 memory
- session 不等于 memory
- skill 不是 memory 的别名

## 6. 非目标

- 不把所有历史都收进 memory
- 不把 memory 设计成黑箱自动学习结果
- 不让 memory 替代 reviewable evidence

## 7. Acceptance

- memory 与 evidence / session / skill 的边界可被解释
- 进入 memory 的东西具有长期团队状态意义
- 下游 continuity design 不需要再猜 memory 的 owner 语义
