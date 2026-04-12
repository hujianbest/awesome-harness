# F100: Agent Teams Product Surface

- Feature ID: `F100`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage` 作为 `Agent Teams` 工作环境时，产品入口、团队对象和产品表面应该保持哪些稳定能力语义。
- 关联文档:
  - `docs/VISION.md`
  - `docs/GARAGE.md`
  - `docs/architecture/1-garage-system-overview.md`
  - `docs/architecture/10-entry-and-host-injection-layer.md`

## 1. 这份文档回答什么

当用户进入 `Garage` 时，他进入的不是模型面板，而是一个 `Agent Teams` 工作环境。

## 2. 稳定 capability cut

- `Garage Team` 是一等产品对象
- `CLIEntry` 与 `WebEntry` 是独立产品入口
- `HostBridgeEntry` 是能力注入层
- 用户面对的是 team / role / handoff / review，而不是工具开关

## 3. 不负责什么

- 不定义 runtime 内部实现细节
- 不定义具体 pack 的业务语义
