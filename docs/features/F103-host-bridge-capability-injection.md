# F103: Host Bridge Capability Injection

- Feature ID: `F103`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `HostBridgeEntry` 作为能力注入层的稳定产品语义。

## 1. 这份文档回答什么

已有工具如何接入 Garage，而不抢走 Garage 的系统真相。

## 2. owner question

当 `Claude`、`OpenCode`、`Cursor` 等工具接入时，哪些能力可以被注入，哪些系统真相不能被宿主拥有。

## 3. 稳定语义

- HostBridge 是 capability injection，不是 product authority
- host 可以提供 hint 与 local context
- host 不能成为 provider truth、pack truth 或 growth truth 的拥有者

## 4. 注入允许项

- agent-facing interactions
- skill invocation surfaces
- local context forwarding
- host-scoped UX affordances

## 5. 注入禁止项

- provider authority override
- pack capability truth override
- session lifecycle redefinition
- workspace fact ownership
- growth / continuity authority override

## 6. 失败语义

当宿主请求越过注入边界时，系统应显式拒绝，而不是静默接受并让 host 逐步成为真相源。

## 7. 非目标

- 不让 HostBridge 变成新的 primary product surface
- 不把 host integration 设计成 developer-only plugin API
- 不要求所有宿主具有相同 UX

## 8. Acceptance

- 宿主可以注入能力，但不能拥有 runtime truth
- host hints 与 local context 不会改写 authority
- HostBridge 与独立工作环境入口共享同一核心主线
