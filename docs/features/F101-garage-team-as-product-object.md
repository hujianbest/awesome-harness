# F101: Garage Team As Product Object

- Feature ID: `F101`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage Team` 为什么是一等产品对象，以及用户与团队的基本关系。

## 1. 这份文档回答什么

用户在 `Garage` 中拥有的到底是什么对象。

## 2. owner question

`Garage Team` 为什么必须先于 model list / tool list 被定义，以及这个对象对用户和系统分别意味着什么。

## 3. 稳定语义

- 用户进入的是自己的 `Garage Team`
- team 高于 model list / tool list / provider toggles
- role / handoff / review / memory / skill 都围绕 team 组织

## 4. 对用户的语义

- 用户拥有并培养的是一个 team
- 用户面对的是 team-level work environment
- 用户与 team 的关系先于与单个 model/tool 的关系

## 5. 对系统的语义

- team 是 runtime 中稳定存在的组织对象
- session、governance、continuity、packs 都围绕 team 组织
- team 不是聊天线程的别名

## 6. 非目标

- 不把 `Garage Team` 退化成品牌文案
- 不把 `Garage Team` 简化成“多个 agent 的列表”
- 不让 provider toggles 成为第一产品对象

## 7. Acceptance

- `Garage Team` 在产品层和系统层都有清楚定义
- 下游 design 不需要再猜“用户拥有的是什么”
- team / role / handoff / review / memory / skill 的关系有共同主语
