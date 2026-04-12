# F121: Neutral Runtime Records

- Feature ID: `F121`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 Garage Team runtime 中立 records 的稳定语义。

## 1. 这份文档回答什么

哪些 runtime records 必须保持中立，才能支撑 team/workspace/governance/growth 主线而不被某个能力面污染。

## 2. owner question

core record vocabulary 的 owner 是谁，以及 pack-local nouns 应该在哪里被挡住。

## 3. 稳定语义

- core records stay neutral
- records must not leak pack-local nouns into core
- records anchor session, evidence, and continuity flows

## 4. 最小记录族

至少应有下面几类中立记录：

- session-intent-like records
- session-state-like records
- context / pointer-like records
- evidence / lineage-like records
- policy / decision-like records

## 5. 边界规则

- records 可以承接 capability refs，但不承接 pack 业务术语
- records 可以被 packs 引用，但不能被 packs 改写成私有 schema 体系
- records 必须能同时被 governance、routing、growth 读取

## 6. 非目标

- 不把 records 变成某个 pack 的领域模型
- 不把 records 和具体文件格式、UI 表示强绑定

## 7. Acceptance

- runtime records 仍然是中立对象
- 关键主线都能共享同一组记录对象
- pack-local 词汇不会反向进入 core records
