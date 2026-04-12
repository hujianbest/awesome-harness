# F11: Runtime Topology And Entry Bootstrap

- Feature ID: `F11`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `runtime home / workspace / entry bootstrap` 的稳定 capability family，确保不同入口都进入同一条启动链。
- 关联文档:
  - `docs/architecture/10-entry-and-host-injection-layer.md`
  - `docs/architecture/11-runtime-coordination-layer.md`
  - `docs/architecture/101-bootstrap-and-profiles.md`
  - `docs/features/F111-runtime-home-and-workspace-topology.md`
  - `docs/features/F112-bootstrap-and-runtime-profile.md`
  - `docs/features/F113-session-api-and-shared-entry-binding.md`

## 1. 这份文档回答什么

Garage 的入口如何在不分叉系统真相的前提下进入同一个 runtime。

## 2. owner question

哪些 capability 属于 shared topology and bootstrap family，哪些只是某个入口自己的 UX 细节。

## 3. stable capability family

- `runtime home`
- `workspace`
- `Bootstrap`
- `RuntimeProfile`
- `SessionApi`
- shared entry binding for CLI / Web / HostBridge

## 4. family 内部关系

- `F102` 负责解释独立工作环境入口
- `F103` 负责解释 HostBridge 作为 capability injection
- `F113` 负责把三类入口汇入同一条 `SessionApi` 主链
- `F111` 与 `F112` 负责 topology 与 authority baseline

因此，本 family 的核心不是“入口功能列表”，而是：

- topology truth
- bootstrap truth
- entry binding truth

## 5. 非目标

- 不定义具体 Web UX
- 不定义具体 CLI 参数表
- 不让某一个入口自己的展示层变成主线 owner

## 6. 下游 specs

- `F111`：runtime home 与 workspace 拓扑
- `F112`：bootstrap 与 runtime profile authority
- `F113`：SessionApi 与 shared entry binding
