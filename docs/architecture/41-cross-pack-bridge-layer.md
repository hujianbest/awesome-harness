# 41: Cross-Pack Bridge Layer

- Architecture Level: `L1`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 回答不同 pack 之间如何做显式 handoff，而不是靠隐式聊天上下文完成跨能力协作。
- 关联文档:
  - `docs/architecture/40-pack-platform-and-extension-layer.md`
  - `docs/architecture/111-cross-pack-bridge-protocol.md`

## 1. owner question

一个 `Garage Team` 在跨 pack 工作时，如何保持 handoff、acceptance、rework 和 lineage 清晰可追溯。

## 2. 关键判断

- bridge is a seam, not a privileged contract
- cross-pack handoff must be materialized on workspace facts
- acceptance and rework must stay visible to governance and evidence

## 3. 非目标

- 不把 bridge 变成新的 core 类型系统
- 不把跨 pack 协作退化成“继续聊天”
