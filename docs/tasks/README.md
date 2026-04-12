# T000: Garage Implementation Tracks

- Task ID: `T000`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: `docs/tasks/` 负责把当前 `Garage` 的产品定义、architecture 主线与 feature families 拆成 implementation slices。它解释“先做什么、后做什么”，但不反向拥有系统真相。
- 当前阶段: architecture / features 已按新主线重建，任务树待下一轮进一步重切
- 关联文档:
  - `docs/README.md`
  - `docs/GARAGE.md`
  - `docs/ROADMAP.md`
  - `packs/README.md`

## 1. 这组文档回答什么

`docs/tasks/` 不再解释 `Garage` 是什么系统，而是回答这些执行问题：

- 应该先做什么，后做什么
- 哪些任务可以并行，哪些必须串行
- 每个 delivery slice 交付什么
- 当前实现如何对齐新的 architecture / features 主线

一句话说：

**`docs/architecture/`、`docs/design/`、`docs/features/` 解释系统真相，`docs/tasks/` 解释当前交付顺序。**

## 2. 当前阅读方式

在读取任务文档前，先读：

1. `docs/VISION.md`
2. `docs/GARAGE.md`
3. `docs/architecture/`
4. `docs/features/`
5. 再回到 `docs/tasks/README.md`

## 3. 当前任务树状态

当前 `T010-T230` 这套任务树，是在上一轮 architecture / features 主线上逐步长出来的实现切片。

由于本轮已经重建了：

- `docs/architecture/`
- `docs/features/`

因此当前任务树应被理解为：

- **有效的实现历史**
- **仍有参考价值的 delivery slices**
- **但已经需要下一轮按新 architecture / features 主线重切**

## 4. 当前 implementation tracks

| Track | Task IDs | 目标 |
| --- | --- | --- |
| Runtime Foundations | `T010-T060` | 搭基础 runtime skeleton、团队主线、governance、workspace facts 与 continuity baseline |
| Reference Packs And Bridge | `T070-T100` | 搭 reference packs 与当前 cross-pack bridge |
| Standalone Runtime Surfaces | `T110-T130` | 把 repo-local 形态推进到 shared runtime topology、bootstrap 与 execution |
| Entry Surfaces And Runtime Productization | `T140-T170` | 把 CLI / Web / HostBridge 与 shared authority 主线推进到可运行产品入口 |
| Runtime Hardening And Delivery | `T180-T201` | 把 authority、secrets、distribution、release、ops 与 trace surface 补成更完整的 runtime 产品基线 |
| Entry Depth And Product Surfaces | `T210-T222` | 继续深化具体 host adapters 与 Web product surfaces |
| Optional Runtime Orchestration | `T230` | 只在需要时再补 supervisor / daemon / multi-workspace orchestration |

## 5. 当前 guardrails

所有 task docs 默认继承下面这些约束：

- task docs 跟随设计真相，不反向定义架构
- `Markdown-first`
- `file-backed`
- `workspace-first`
- `one runtime, many entry surfaces`
- `Agent Teams workspace` 优先于工具开关视角
- `Garage Team runtime` 必须高于单一入口存在
- packs 只声明 capabilities，不绑定 vendors
- provider authority 由 runtime 配置链主导，host 只能提供 hint
- `evidence -> proposal -> governance -> update` 是 canonical growth loop

## 6. 下一轮任务重切建议

由于 architecture / features 已经整体重建，建议下一轮优先做：

1. 按新的 `L0/L1/L2` architecture 主线，重切 `T010-T100`
2. 按新的 feature families，重切 `T110-T170`
3. 再判断 `T180-T230` 中哪些可直接继承，哪些也需要重切

## 7. 当前代码进度快照（handoff 用，非架构真相）

本节只回答「仓库里已经有什么」，不替代新的 architecture / features 主线。

| 范围 | 本仓库实现情况 | 说明 |
| --- | --- | --- |
| `T140-T170` | 已有对应实现 | CLI、HostBridge、Web control plane 骨架、runtime-home authority loader |
| `T180-T212` | 已有较明确实现 | secrets、doctor、distribution、release smoke、ops、trace surface、具体 host adapter 守卫 |
| `T220-T222`、`T230` | 未在本周期完整落地 | Web streaming / observability / governance UI 与 optional daemon 仍待后续切片 |

## 8. 维护约定

- task docs 保持执行导向，不重复设计文档里的长篇论证。
- architecture / features 主线如果重切，任务树应跟着重切。
- 新增 task doc 时，先更新本页索引与依赖顺序。
- 如果某个 task 已经明显变成稳定 capability 或系统语义，应把真相源提升回 `docs/features/` 或 `docs/architecture/`。
