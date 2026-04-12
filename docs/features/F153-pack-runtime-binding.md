# F153: Pack Runtime Binding

- Feature ID: `F153`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 packs、registry 和 runtime 之间的绑定语义。

## 1. 这份文档回答什么

pack 在被发现之后，如何真正绑定到 `Garage Team runtime`，以及哪些绑定关系必须显式存在。

## 2. owner question

谁负责把 contracts / registry 的发现结果，变成 session / execution / governance 可用的 runtime binding。

## 3. 稳定语义

- runtime binds packs through contracts and registry
- binding stays explicit and inspectable
- pack-local language must not leak into core

## 4. 最小绑定关系

- pack to session
- pack to role / node set
- pack to artifact routing surface
- pack to governance scope
- pack to execution capability surface

## 5. 边界规则

- discovery 不等于 binding
- binding 不等于 execution
- pack binding 可以影响 capability surface，但不能改写 core record model

## 6. 非目标

- 不让每个 pack 自己维护私有 runtime binding layer
- 不让 binding 结果成为不可检查的黑箱状态

## 7. Acceptance

- pack 绑定关系可被解释和检查
- session / governance / execution 可共享同一 binding 结果
- pack-local 术语不会反向污染核心绑定语义
