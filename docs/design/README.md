# D000: Garage Design

- Design ID: `D000`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: `docs/design/` 用来承接 `Garage` 在产品与实现之间的详细设计层，解释跨 pack 产品/交互设计、入口产品设计、治理与成长体验设计，以及 pack 或子系统级详细设计。

## 1. 这组文档回答什么

`docs/design/` 不重复回答：

- 为什么要做 `Garage`
- `Garage` 当前是什么产品
- `Garage Team runtime` 的顶层架构是什么
- 系统必须具备哪些稳定 capability families

这些分别属于：

- `docs/VISION.md`
- `docs/GARAGE.md`
- `docs/architecture/`
- `docs/features/`

`docs/design/` 只回答更靠近“怎么被体验、怎么被使用、怎么被具体设计”的问题。

## 2. 设计层的四类文档

| 层次 | 编号 | 用途 |
| --- | --- | --- |
| Cross-pack product / interaction | `D10-D19` | 跨 pack 的产品设计、交互模型、团队体验、一致性约束 |
| Entry product design | `D20-D29` | CLI / Web / HostBridge 的入口产品设计 |
| Governance / growth experience | `D30-D39` | workspace facts、evidence、治理、成长相关体验设计 |
| Pack / subsystem detailed design | `D40-D99` | pack 详细设计、bridge authoring、平台 authoring 或子系统细节 |

## 3. 编号规则

- `design` 保留 `D` 前缀
- 顶层 design families 使用 2 位编号，例如 `D10`、`D20`
- 需要更细的详细设计时，使用 3 位编号，例如 `D101`、`D201`
- 编号稳定后不应因为目录整理而重排

## 4. owner 边界

- `docs/design/` 可以补跨 pack 的产品设计 / 交互设计
- `docs/design/` 可以补 pack 或子系统级详细设计
- `docs/design/` 不应反向重写 `docs/architecture/` 的边界
- `docs/design/` 不应反向定义 `docs/features/` 的 capability truth
- `docs/tasks/` 只能跟随这里的设计，不反向拥有设计真相

## 5. 建议阅读顺序

1. `docs/VISION.md`
2. `docs/GARAGE.md`
3. `docs/architecture/`
4. `docs/features/`
5. 再读 `docs/design/`
6. 最后读 `docs/tasks/README.md`

## 6. 当前 design 主线

当前建议优先维护下面这些设计文档：

- `D10-agent-teams-workspace-design.md`
- `D11-multi-entry-parity-and-host-injection-design.md`
- `D12-handoff-review-and-human-gate-design.md`
- `D20-cli-entry-product-design.md`
- `D21-web-entry-product-design.md`
- `D22-host-bridge-product-design.md`
- `D30-workspace-facts-and-evidence-experience.md`
- `D31-growth-memory-skill-experience.md`
- `D40-pack-platform-authoring-design.md`
- `D41-cross-pack-bridge-authoring-design.md`
- `D42-coding-pack-design.md`
- `D43-product-insights-pack-design.md`
