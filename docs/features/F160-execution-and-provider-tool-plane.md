# F160: Execution And Provider Tool Plane

- Feature ID: `F160`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 provider、tool、execution trace 与 authority placement 的稳定 capability cut。
- 关联文档:
  - `docs/architecture/12-execution-and-provider-layer.md`
  - `docs/architecture/103-execution-runtime.md`
  - `docs/architecture/101-bootstrap-and-profiles.md`

## 1. 这份文档回答什么

Garage Team runtime 如何统一执行 provider/tool work，并把 authority 放在正确位置。

## 2. 稳定 capability cut

- provider authority in runtime configuration
- provider/tool execution
- tool capability surface
- execution trace
- evidence-linked execution outcomes

## 3. 不负责什么

- 不让 host 或 packs 成为 provider truth source
- 不让 execution 替代 governance
