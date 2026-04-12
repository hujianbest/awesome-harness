# F132: Artifact Routing

- Feature ID: `F132`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 neutral artifact intent 到权威 workspace surface 的稳定映射语义。

## 1. 这份文档回答什么

neutral artifact intents 如何被映射到 workspace-first 主事实面，以及 routing 与 pack 业务语义如何分离。

## 2. owner question

谁定义 artifact authority、destination 和 write semantics，谁不能越权决定这些东西。

## 3. 稳定语义

- routing maps intent to authoritative destination
- routing stays separate from pack-local business meaning
- routing preserves workspace-first truth

## 4. 最小输入

- artifact intent
- artifact role
- current session / node context
- authority-preserving destination rules

## 5. 最小输出

- authoritative target path
- write semantics
- readback-compatible locator

## 6. 边界规则

- routing 不负责定义业务内容
- routing 不替代 governance 对可信度的判断
- routing 不能把主 artifacts 漂移进 runtime home

## 7. 非目标

- 不把 routing 退化成 pack 自己拼路径的约定
- 不把 artifact authority 隐藏在实现细节里

## 8. Acceptance

- neutral artifact intents 可以被稳定映射到权威 surface
- routing 结果对人类和系统都可解释
- 不同 packs 不需要自己重发明主事实面的落盘规则
