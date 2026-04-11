# T000: Garage Implementation Tracks

- Task ID: `T000`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: `docs/architecture/`、`docs/design/` 与 `docs/features/` 负责解释 `Garage` 的完整系统边界；`docs/tasks/` 负责把这套边界按实施顺序拆成 delivery slices。当前 `T010-T130` 是第一组主要实施切片，`T140-T170` 是第二组围绕三类入口与共享 provider authority 的实施切片，`T180-T230` 是第三组围绕 runtime hardening、具体入口深化与交付运维的实施切片；它们都不再拥有产品主线定义权，只负责承接当前实现顺序。
- 当前阶段: 完整架构主线下的前三组 implementation tracks
- 关联文档:
  - `docs/README.md`
  - `docs/GARAGE.md`
  - `docs/ROADMAP.md`
  - `packs/README.md`

## 1. 这组文档回答什么

这组文档不再重复解释 `Garage` 为什么这样设计，而是回答下面这些执行问题：

- 应该先做什么，后做什么
- 哪些任务可以并行，哪些必须串行
- 每个 delivery slice 要交付什么
- 当前实现如何对齐完整架构

一句话说：

**`docs/architecture/`、`docs/design/`、`docs/features/` 解释系统真相，`docs/tasks/` 解释当前交付顺序。**

## 2. 如何阅读当前任务树

理解这组任务文档时，请先记住下面 4 个判断：

1. 先读 `docs/architecture/`、`docs/features/`、`docs/design/`，再读 `docs/tasks/`。
2. 当前 `T010-T130` 是第一组 implementation tracks，`T140-T170` 是第二组独立入口 implementation tracks，`T180-T230` 是第三组产品化 implementation tracks；它们都不是完整架构的全文镜像。
3. task 文件名已经统一对齐到 `Txxx-<title-slug>.md` 规则，但这些文档仍然只是当前 implementation tracks。
4. 当设计文档和 task 文档冲突时，应先回写设计文档，再重切任务文档。

### 2.1 Handoff 速查（第三组产品化切片）

- **主要代码位置**：`src/bootstrap/`（入口、profile、credentials、doctor、install 默认路径、ops、trace 摘要、具体宿主守卫）、`src/redaction.py`、`src/execution/runtime.py`、`scripts/release_smoke.py`。
- **验证**：`python -m unittest discover -s tests`；发布前可跑 `python scripts/release_smoke.py`。
- **本周期未接**：`T220`–`T222`（WebEntry 深化）、`T230`（supervisor / daemon）——需要 SSE/轮询策略、浏览器侧治理 UX 或多 workspace 编排需求明确后再切。

## 3. 命名规则

- 目录入口使用 `docs/tasks/README.md`
- `docs/tasks/README.md` 保留目录索引入口的 canonical 文件名
- task docs 统一使用稳定 `Txxx` 作为 identity
- 当前 `T010-T230` 保留既有文件路径
- 未来新增 task docs 继续使用 `Txxx-<title-slug>.md`

## 4. 当前 implementation tracks

| Track | Task IDs | 目标 | 主要输入 |
| --- | --- | --- | --- |
| Runtime Foundations | `T010-T060` | 搭基础 runtime skeleton、records、contracts、governance、artifact / evidence surface 与 continuity baseline | `A110`、`A120`、`A130`、`A150`、`F010`、`F030`、`F050`、`F060`、`F070`、`F080` |
| Reference Packs And Bridge | `T070-T100` | 搭 `Product Insights Pack`、`Coding Pack` 与当前 cross-pack bridge | `A160`、`A170`、`F110`、`F120`、`D110`、`D120`、`F070`、`F080` |
| Standalone Runtime Surfaces | `T110-T130` | 把当前 repo-local 形态继续推进到 runtime topology、bootstrap 与 execution layer | `F210`、`F220`、`F230`、`F050`、`F060`、`F080` |
| Entry Surfaces And Runtime Productization | `T140-T170` | 把三类入口从架构 seam 推进到可实现的产品入口，并收敛 shared provider authority | `A120`、`F210`、`F220`、`F230`、`F010` |
| Runtime Hardening And Delivery | `T180-T201` | 把 authority、secrets、配置诊断、分发、发布与运行诊断补成可交付的 runtime 产品基线 | `F210`、`F220`、`F230`、`F050`、`A120`、`A140` |
| Entry Depth And Product Surfaces | `T210-T222` | 把通用入口切到具体宿主适配与更完整的 WebEntry streaming / observability / governance surfaces | `T150`、`T160`、`T170`、`F220`、`F230`、`F050` |
| Optional Runtime Orchestration | `T230` | 只在确有需求时，再补 supervisor / daemon / multi-workspace orchestration | `T191`、`T200`、`T221`、`F210`、`F220` |

## 5. 当前详细交付顺序

| 顺序 | Task ID | 文件 | 当前角色 | 主要依赖 |
| --- | --- | --- | --- | --- |
| 01 | `T010` | `docs/tasks/T010-garage-foundation-and-repository-layout.md` | 第一组 runtime foundation 的仓库骨架与边界起点 | `A110-garage-extensible-architecture.md` |
| 02 | `T020` | `docs/tasks/T020-garage-core-runtime-records.md` | 落 `Garage Core` 的运行时对象与记录语义 | `F030-core-runtime-records.md` |
| 03 | `T030` | `docs/tasks/T030-garage-shared-contracts-and-registry.md` | 落 shared contracts、校验、加载与 registry | `A160-garage-pack-platform-architecture.md`、`F010-shared-contracts.md`、`F020-shared-contract-schemas.md` |
| 04 | `T040` | `docs/tasks/T040-garage-session-lifecycle-and-governance.md` | 落 session 主链、handoff、gate、approval 与 exception | `A150-garage-vision-and-governance-architecture.md`、`F040-session-lifecycle-and-handoffs.md`、`F050-governance-model.md` |
| 05 | `T050` | `docs/tasks/T050-garage-artifact-routing-and-evidence-surface.md` | 落 workspace-first artifact / evidence surface | `F060-artifact-and-evidence-surface.md` |
| 06 | `T060` | `docs/tasks/T060-garage-continuity-and-promotion.md` | 落 continuity、promotion baseline 与学习 loop 的第一层实现切片 | `A130-garage-continuity-memory-skill-architecture.md`、`F070-continuity-mapping-and-promotion.md`、`F080-garage-self-evolving-learning-loop.md` |
| 07 | `T070` | `docs/tasks/T070-garage-reference-pack-shells.md` | 搭两个 reference packs 的共同骨架 | `A160-garage-pack-platform-architecture.md`、`F110-reference-packs.md` |
| 08 | `T080` | `docs/tasks/T080-garage-product-insights-pack.md` | 落 `Product Insights Pack`，并对齐成长 loop 的 candidate mapping | `A160-garage-pack-platform-architecture.md`、`D110-garage-product-insights-pack-design.md`、`F070-continuity-mapping-and-promotion.md`、`F080-garage-self-evolving-learning-loop.md` |
| 09 | `T090` | `docs/tasks/T090-garage-coding-pack.md` | 落 `Coding Pack`，并对齐成长 loop 的 candidate mapping | `A160-garage-pack-platform-architecture.md`、`D120-garage-coding-pack-design.md`、`F070-continuity-mapping-and-promotion.md`、`F080-garage-self-evolving-learning-loop.md` |
| 10 | `T100` | `docs/tasks/T100-garage-cross-pack-bridge-and-walkthrough.md` | 打通当前 reference packs 主桥并做端到端走通 | `A170-garage-cross-pack-bridge-architecture.md`、`F120-cross-pack-bridge.md` |
| 11 | `T110` | `docs/tasks/T110-garage-runtime-home-and-workspace-topology.md` | 把 repo-local dogfooding 形态提升成显式 `runtime home / workspace` 拓扑 | `F210-runtime-home-and-workspace-topology.md`、`F060-artifact-and-evidence-surface.md` |
| 12 | `T120` | `docs/tasks/T120-garage-runtime-bootstrap-and-entrypoints.md` | 落统一 launcher、profile / workspace / host binding 与 create / resume 启动链 | `F220-runtime-bootstrap-and-entrypoints.md`、`F210-runtime-home-and-workspace-topology.md` |
| 13 | `T130` | `docs/tasks/T130-garage-runtime-provider-and-tool-execution.md` | 落 provider adapters、tool registry、execution trace 与受治理的 runtime execution layer | `F230-runtime-provider-and-tool-execution.md`、`F080-garage-self-evolving-learning-loop.md` |
| 14 | `T140` | `docs/tasks/T140-garage-stable-cli-shell.md` | 把 `CLIEntry` 落成最薄、稳定、可恢复的统一命令入口 | `F220-runtime-bootstrap-and-entrypoints.md`、`F210-runtime-home-and-workspace-topology.md`、`A120-garage-core-subsystems-architecture.md` |
| 15 | `T150` | `docs/tasks/T150-garage-host-bridge-entry.md` | 把宿主集成收敛到通用 `HostBridgeEntry` 与薄适配层 | `F220-runtime-bootstrap-and-entrypoints.md`、`F230-runtime-provider-and-tool-execution.md`、`F010-shared-contracts.md` |
| 16 | `T160` | `docs/tasks/T160-garage-local-first-web-control-plane.md` | 落 local-first `WebEntry` control plane，让 UI 消费共享 runtime seam | `F220-runtime-bootstrap-and-entrypoints.md`、`F210-runtime-home-and-workspace-topology.md`、`F230-runtime-provider-and-tool-execution.md` |
| 17 | `T170` | `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md` | 落 `runtime home` 内 provider / profile loader 与 authority resolution | `F210-runtime-home-and-workspace-topology.md`、`F220-runtime-bootstrap-and-entrypoints.md`、`F230-runtime-provider-and-tool-execution.md` |
| 18 | `T180` | `docs/tasks/T180-garage-secrets-and-credential-resolution.md` | 落 `RuntimeProfile` 与 adapters 的 secrets / credential resolution seam | `T170-garage-provider-profile-loader-and-authority-resolution.md`、`F210-runtime-home-and-workspace-topology.md`、`F230-runtime-provider-and-tool-execution.md` |
| 19 | `T181` | `docs/tasks/T181-garage-runtime-home-config-doctor.md` | 落 runtime home config 校验、doctor UX 与安全迁移钩子 | `T170-garage-provider-profile-loader-and-authority-resolution.md`、`F210-runtime-home-and-workspace-topology.md` |
| 20 | `T190` | `docs/tasks/T190-garage-distribution-and-install-layout.md` | 落 CLI 分发、安装布局、版本化与升级路径 | `T140-garage-stable-cli-shell.md`、`T170-garage-provider-profile-loader-and-authority-resolution.md`、`T180-garage-secrets-and-credential-resolution.md` |
| 21 | `T191` | `docs/tasks/T191-garage-release-smoke-and-compatibility-matrix.md` | 落 release smoke checks 与 host / OS 兼容矩阵 | `T190-garage-distribution-and-install-layout.md` |
| 22 | `T200` | `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md` | 落 runtime ops baseline、structured logs、diagnostics 与 local health surface | `T170-garage-provider-profile-loader-and-authority-resolution.md`、`T180-garage-secrets-and-credential-resolution.md`、`F230-runtime-provider-and-tool-execution.md` |
| 23 | `T201` | `docs/tasks/T201-garage-execution-trace-and-evidence-ops-surface.md` | 落 execution trace / evidence 的运维观察面 | `T200-garage-runtime-ops-and-diagnostics.md`、`T130-garage-runtime-provider-and-tool-execution.md`、`F060-artifact-and-evidence-surface.md` |
| 24 | `T210` | `docs/tasks/T210-garage-host-adapter-cursor.md` | 把 `Cursor` 落成具体 `HostBridgeEntry` adapter | `T150-garage-host-bridge-entry.md` |
| 25 | `T211` | `docs/tasks/T211-garage-host-adapter-claude.md` | 把 `Claude` 落成具体 `HostBridgeEntry` adapter | `T150-garage-host-bridge-entry.md` |
| 26 | `T212` | `docs/tasks/T212-garage-host-adapter-opencode.md` | 把 `OpenCode` 落成具体 `HostBridgeEntry` adapter | `T150-garage-host-bridge-entry.md` |
| 27 | `T220` | `docs/tasks/T220-garage-webentry-streaming-and-live-updates.md` | 为 `WebEntry` 增加 streaming 与 live session updates | `T160-garage-local-first-web-control-plane.md`、`T170-garage-provider-profile-loader-and-authority-resolution.md` |
| 28 | `T221` | `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md` | 为 `WebEntry` 增加 observability、runs、traces 与错误观察面 | `T160-garage-local-first-web-control-plane.md`、`T200-garage-runtime-ops-and-diagnostics.md` |
| 29 | `T222` | `docs/tasks/T222-garage-webentry-governance-and-review-surfaces.md` | 为 `WebEntry` 增加 review、approval 与 governance surfaces | `T160-garage-local-first-web-control-plane.md`、`F050-governance-model.md`、`T040-garage-session-lifecycle-and-governance.md` |
| 30 | `T230` | `docs/tasks/T230-garage-runtime-supervisor-and-multi-workspace-daemon.md` | 在确有需求时补 supervisor / daemon / multi-workspace orchestration | `T191-garage-release-smoke-and-compatibility-matrix.md`、`T221-garage-webentry-observability-and-traces-ui.md`、`F210-runtime-home-and-workspace-topology.md` |

## 6. 当前 implementation guardrails

所有 task docs 默认继承下面这些约束：

- task docs 跟随设计真相，不反向定义架构
- `Markdown-first`
- `file-backed`
- `Contract-first`
- core 只理解中立对象，不吸收 pack 领域词
- 新增能力优先通过 pack 扩展，而不是修改 core 语义
- `evidence -> proposal -> governance -> update` 是 canonical growth loop
- workspace-first growth 优先于全局自动共享
- 不新增独立 `BridgeContract`
- one runtime, many entry surfaces
- entry-facing 请求复用同一条 `Bootstrap -> SessionApi -> Session` 主链
- `workspace facts` 不被 `runtime home` 吞并
- packs 只声明 capabilities，不绑定 vendors
- provider / model authority 由 `RuntimeProfile` 主导，host 只提供提示
- provider differences stay below core

## 7. 设计到任务的映射

| 设计文档 | 当前主要落到哪些 task docs |
| --- | --- |
| `A110-garage-extensible-architecture.md` | `T010`、`T070` |
| `A120-garage-core-subsystems-architecture.md` | `T010`、`T020`、`T030`、`T040`、`T050`、`T120`、`T130`、`T140`、`T150`、`T160`、`T170`、`T180`、`T181`、`T190`、`T200` |
| `A130-garage-continuity-memory-skill-architecture.md` | `T060` |
| `A140-garage-system-architecture.md` | 作为全部切片的 system-level 对齐输入，尤其影响 `T190-T230` 的产品化顺序 |
| `A150-garage-vision-and-governance-architecture.md` | `T040`、`T060`、`T100` |
| `A160-garage-pack-platform-architecture.md` | `T030`、`T070`、`T080`、`T090`、`T100` |
| `A170-garage-cross-pack-bridge-architecture.md` | `T100` |
| `F220-runtime-bootstrap-and-entrypoints.md` | `T120`、`T140`、`T150`、`T160`、`T170`、`T190`、`T210`、`T211`、`T212`、`T220`、`T221`、`T222`、`T230` |
| `F230-runtime-provider-and-tool-execution.md` | `T130`、`T150`、`T160`、`T170`、`T180`、`T190`、`T200`、`T201`、`T220`、`T221` |
| `F210-runtime-home-and-workspace-topology.md` | `T110`、`T120`、`T140`、`T160`、`T170`、`T180`、`T181`、`T190`、`T230` |
| `F030-core-runtime-records.md` | `T020` |
| `F040-session-lifecycle-and-handoffs.md` | `T040`、`T100` |
| `F050-governance-model.md` | `T040`、`T060`、`T100`、`T130`、`T180`、`T200`、`T222` |
| `F060-artifact-and-evidence-surface.md` | `T050`、`T100`、`T110`、`T130`、`T201`、`T221` |
| `F010-shared-contracts.md` | `T030`、`T070`、`T120`、`T150` |
| `F020-shared-contract-schemas.md` | `T030` |
| `F070-continuity-mapping-and-promotion.md` | `T060`、`T080`、`T090` |
| `F080-garage-self-evolving-learning-loop.md` | `T060`、`T080`、`T090`、`T130` |
| `F110-reference-packs.md` | `T070` |
| `D110-garage-product-insights-pack-design.md` | `T080` |
| `D120-garage-coding-pack-design.md` | `T090` |
| `F120-cross-pack-bridge.md` | `T100` |

## 8. 后续重切建议

当前任务树已经把第三组产品化切片切成 `T180-T230`。在这组切片稳定后，建议优先重切下面这些方向：

- 为 `runtime update / growth promotion / continuity stores` 补更明确的交付切片
- 为 package signing、artifact provenance 与 release automation 继续细分 release tracks
- 为 `WebEntry` 的 authn/authz、local security hardening 与 browser persistence 再切更深任务
- 如果具体宿主 adapter 出现明显分叉，再继续把 `Cursor`、`Claude`、`OpenCode` 下钻为更细的 integration slices

## 9. 维护约定

- task docs 保持执行导向，不重复设计文档里的长篇论证。
- 设计变更优先回写 `docs/architecture/`、`docs/design/` 或 `docs/features/`；任务变更优先回写 `docs/tasks/`。
- 新增 task doc 时，先更新本页索引与依赖顺序。
- 如果某个 task 已经明显变成独立 capability 或稳定系统语义，应把真相源提升回 `docs/features/` 或 `docs/architecture/`，而不是继续堆在 task doc 里。

## 10. 代码进度快照（handoff 用，非架构真相）

本节只回答「仓库里已经有什么」，**不**替代上文交付顺序与 `docs/features/`、`docs/architecture/` 的语义定义。

| 范围 | 本仓库实现情况 | 说明 |
| --- | --- | --- |
| `T180`–`T181` | 已有对应实现 | 凭据引用解析、`garage doctor`、迁移版本文件提示 |
| `T190`–`T191` | 已有对应实现 | 默认 runtime home / 环境变量覆盖、`garage --version`、`scripts/release_smoke.py` |
| `T200`–`T201` | 已有对应实现 | `garage status`、launcher ops 事件、`summarize_execution_trace` / `SessionApi.summarize_step_outcome` |
| `T210`–`T212` | 已有对应实现 | `require_cursor_host_bridge` 等具体宿主守卫，仍走共享 `HostBridgeSessionApi` |
| `T220`–`T222`、`T230` | 未在本周期落地 | Web streaming/观测/治理 UI 与可选 daemon 待后续切片 |
