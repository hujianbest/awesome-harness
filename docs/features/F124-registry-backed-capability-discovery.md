# F124: Registry-Backed Capability Discovery

- Feature ID: `F124`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 registry-backed capability discovery 的稳定语义。

## 1. 这份文档回答什么

runtime 如何发现并解释 packs、roles、nodes、artifact roles 与 capability surfaces，而不把 discovery 和 execution / governance 混在一起。

## 2. owner question

哪些东西属于 discovery，哪些东西属于后续 binding、governance 和 execution。

## 3. 稳定语义

- runtime discovers capabilities through registry
- registry binds teams to packs through contracts
- discovery stays separate from execution and governance decisions

## 4. 最小发现对象

- pack
- role
- node
- artifact role
- evidence role or requirement anchor
- capability declaration

## 5. 边界规则

- registry 负责发现和校验，不负责执行
- registry 可以暴露 capability surfaces，但不拥有 provider authority
- registry 结果应能被 session、governance、routing 和 execution 共用

## 6. 非目标

- 不把 registry 设计成远程市场
- 不让 registry 退化成 pack 私有加载器集合

## 7. Acceptance

- capability discovery 与 execution / governance / binding 的边界清楚
- runtime 可以共享一套 registry 解释不同能力面
- packs 通过 registry 接入，而不是各自发明私有发现链
