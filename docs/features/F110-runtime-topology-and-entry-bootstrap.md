# F110: Runtime Topology And Entry Bootstrap

- Feature ID: `F110`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `runtime home / workspace / entry bootstrap` 的稳定 capability cut，确保不同入口都进入同一条启动链。
- 关联文档:
  - `docs/architecture/10-entry-and-host-injection-layer.md`
  - `docs/architecture/11-runtime-coordination-layer.md`
  - `docs/architecture/101-bootstrap-and-profiles.md`

## 1. 这份文档回答什么

Garage 的入口如何在不分叉系统真相的前提下进入同一个 runtime。

## 2. 稳定 capability cut

- `Bootstrap`
- `RuntimeProfile`
- `runtime home`
- `workspace`
- `SessionApi`
- shared entry binding for CLI / Web / HostBridge

## 3. 不负责什么

- 不定义 provider/tool invocation 细节
- 不定义长期 continuity 规则
