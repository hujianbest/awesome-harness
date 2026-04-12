# F151: Pack Platform

- Feature ID: `F151`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 pack platform 的稳定语义。

## 1. 这份文档回答什么

Garage Team 如何通过 pack platform 吸收新能力面，而不把 platform 退化成静态插件市场。

## 2. owner question

哪些扩展属于 pack platform，哪些仍然属于 core truth、governance truth 或 entry truth。

## 3. 稳定语义

- packs extend team capability
- pack platform binds extension into runtime through stable seams
- packs do not redefine platform truth

## 4. 最小平台职责

- 接入新的 capability domains
- 通过 contracts / registry 完成绑定
- 让新能力面能复用 team / session / evidence / growth 主线

## 5. 边界规则

- pack platform 不拥有 provider truth
- pack platform 不改写 team runtime core
- pack platform 不替代 governance

## 6. 非目标

- 不把 pack platform 设计成 marketplace first
- 不把 packs 当成系统真相源

## 7. Acceptance

- 新能力面可以通过 pack 进入系统
- packs 不需要改 core 语义就能扩展团队能力
- 平台和能力面边界保持清楚
