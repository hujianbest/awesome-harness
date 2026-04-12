# F154: Cross-Pack Bridge

- Feature ID: `F154`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 cross-pack bridge 的稳定语义。

## 1. 这份文档回答什么

两个 capability domains / packs 在一个 `Garage Team` 中协作时，bridge seam 如何显式成立。

## 2. owner question

跨 pack handoff、acceptance、rework 和 lineage 的稳定语义由谁定义，哪些东西不能退回成“继续聊天”。

## 3. 稳定语义

- bridge is a seam, not a privileged core contract
- handoff must materialize as artifacts and evidence
- acceptance, rework, and lineage remain explicit

## 4. 最小 bridge 对象

- handoff payload
- bridge artifact surface
- acceptance verdict
- rework request
- lineage link

## 5. 边界规则

- cross-pack bridge 不等于 team 内普通 handoff
- bridge 必须显式留下 artifacts / evidence
- bridge 不能成为新的 privileged core contract

## 6. 非目标

- 不让 bridge 退化成聊天上下文流转
- 不让 bridge 自己拥有 provider / pack authority

## 7. Acceptance

- 跨 pack handoff 可以被显式记录、接受、退回和追踪
- bridge 对 governance 与 evidence 可见
- `F123` 和 `F154` 的边界不再模糊
