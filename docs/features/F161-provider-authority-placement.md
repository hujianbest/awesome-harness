# F161: Provider Authority Placement

- Feature ID: `F161`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 provider / model authority 应放在哪里的稳定语义。

## 1. 这份文档回答什么

provider / model authority 应该放在哪里，谁可以给 hint，谁不能成为真相源。

## 2. owner question

在 `Garage Team runtime` 中，provider authority 究竟由 `RuntimeProfile`、host、pack 还是执行层拥有。

## 3. 稳定语义

- provider authority lives in runtime configuration
- packs do not own vendors
- hosts do not become provider truth sources

## 4. authority 顺序

- runtime configuration / `RuntimeProfile`
- non-authoritative host hints
- downstream execution selection

## 5. 边界规则

- packs declare capabilities, not vendors
- hosts may constrain or hint, but not own provider truth
- execution can consume authority, but not create it

## 6. 非目标

- 不把 provider 选择权给 pack manifest
- 不让 host integration 变成主配置入口
- 不让 execution runtime 自己发明 authority

## 7. Acceptance

- provider authority 有单一 owner
- host 和 packs 不再与 runtime configuration 争夺 authority
- 下游 design 不需要再猜测 provider truth 的 owner
