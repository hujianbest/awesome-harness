# `agent-skills-main` 与 `ahe-*` workflow skills 对比报告

## 结论摘要

- `agent-skills-main` 更像一个“可分发、可移植、可上手”的通用工程 skill 产品包。它的强项是统一 anatomy、元 skill 路由、命令/agent/hook 配套，以及较低的理解门槛。核心证据见 `references/agent-skills-main/README.md`、`references/agent-skills-main/docs/skill-anatomy.md`、`references/agent-skills-main/skills/using-agent-skills/SKILL.md`。
- `ahe-*` 更像一个“强约束、强证据、强交接”的软件交付工作流家族。它的强项是状态机式编排、profile-aware 节点链路、显式工件契约，以及 review/gate 串联。核心证据见 `skills/ahe-workflow-starter/SKILL.md`、`skills/ahe-test-driven-dev/SKILL.md`、`skills/ahe-regression-gate/SKILL.md`、`skills/ahe-completion-gate/SKILL.md`、`skills/ahe-finalize/SKILL.md`。
- 如果目标是继续把 AHE 打造成个人 harness engineering 工作台，最该借鉴的不是 `agent-skills-main` 的通用覆盖广度，而是它的“统一入口 + 统一 anatomy + 统一辅助资产 + 低摩擦加载”。
- 如果目标是让 AHE 更容易对外复用或跨仓库采用，当前最大阻力不是能力不够，而是认知负担高、模板契约未完全统一、对仓库目录与状态工件耦合较深。

## 对比范围

- `references/agent-skills-main` 全量 skill 目录与入口文档
- `skills/ahe-*/SKILL.md` 全量 workflow skills
- `skills/README.md`
- `skills/design_rules.md`
- `templates/task-progress-template.md`
- 代表性 `agent-skills-main` 文件：
  - `references/agent-skills-main/README.md`
  - `references/agent-skills-main/docs/skill-anatomy.md`
  - `references/agent-skills-main/skills/using-agent-skills/SKILL.md`
  - `references/agent-skills-main/.claude/commands/build.md`
  - `references/agent-skills-main/.claude/commands/review.md`
  - `references/agent-skills-main/agents/code-reviewer.md`
  - `references/agent-skills-main/hooks/hooks.json`
  - `references/agent-skills-main/hooks/session-start.sh`
- 代表性 AHE 文件：
  - `skills/ahe-workflow-starter/SKILL.md`
  - `skills/ahe-specify/SKILL.md`
  - `skills/ahe-tasks/SKILL.md`
  - `skills/ahe-tasks-review/SKILL.md`
  - `skills/ahe-test-driven-dev/SKILL.md`
  - `skills/ahe-regression-gate/SKILL.md`
  - `skills/ahe-completion-gate/SKILL.md`
  - `skills/ahe-finalize/SKILL.md`

## 系统定位对比

| 维度 | `agent-skills-main` | `ahe-*` | 判断 |
| --- | --- | --- | --- |
| 主要目标 | 通用工程 skill 产品包 | AHE 内部软件交付 workflow 家族 | 两者目标不同，不能只按“功能多少”评价 |
| 复用单元 | 单 skill 可独立触发，也可被命令串联 | 单节点 skill，默认通过 `ahe-workflow-starter` 统一编排 | `agent-skills` 更像工具箱，AHE 更像流程机 |
| 路由方式 | `using-agent-skills` 元 skill + `.claude/commands/*.md` + SessionStart hook | `ahe-workflow-starter` 做阶段判断、profile 判断与迁移 | AHE 路由更强约束，`agent-skills` 更轻量 |
| 生命周期模型 | DEFINE / PLAN / BUILD / VERIFY / REVIEW / SHIP | full / standard / lightweight 主链 + increment / hotfix 支线 | `agent-skills` 易懂，AHE 更贴近真实交付 |
| 证据模型 | Verification checklist + review persona + command wrapper | review record + verification record + task-progress + explicit handoff | AHE 的证据链更完整、更可审计 |
| 人工介入 | 偏建议式与验证式，人类可随时介入 | spec/design 审批、测试设计确认等处有明确 pause point | AHE 更适合高控制场景，自动化摩擦更大 |
| 辅助资产 | `docs/skill-anatomy.md`、`agents/`、`.claude/commands/`、`hooks/`、`references/` | `templates/` + 各 skill 的 `references/` + repo 级 `AGENTS.md` | `agent-skills` 的配套层更完整 |
| 可移植性 | 高，默认就是可分发 skill pack | 中等偏低，对目录、记录路径和状态工件假设较强 | AHE 若要跨 repo 复用，还需要一层抽象 |
| 维护成本 | 中等，靠统一 anatomy 降低漂移 | 偏高，starter 过重且跨 skill 有重复规则 | AHE 更容易出现一致性漂移 |

## `agent-skills-main` 的优势

- 有真正的家族级元 skill。`references/agent-skills-main/skills/using-agent-skills/SKILL.md` 不只是“入口说明”，而是集中定义了路由图、全局行为约束、失败模式和典型 skill 序列。
- 有清晰且可复用的 skill anatomy。`references/agent-skills-main/docs/skill-anatomy.md` 明确 frontmatter、标准章节、supporting files、命名和交叉引用规则，使整个 skill 库更容易扩展和外部理解。
- skill 粒度兼容“独立调用 + 串联调用”两种模式。`spec-driven-development`、`planning-and-task-breakdown`、`incremental-implementation`、`test-driven-development` 等既能单独使用，也能被 `.claude/commands/build.md` 这类薄命令包装串联。
- 配套资产比较完整。`.claude/commands/` 提供命令入口，`agents/code-reviewer.md` 等 persona 提供角色视角，`hooks/session-start.sh` 通过 SessionStart 自动注入元 skill，显著降低“应该先用哪个 skill”的心智负担。
- “反合理化”设计被当成第一类能力来写。多数 skill 都有 `Common Rationalizations` 或等价结构，这能显著降低 agent 因为图省事而跳过关键步骤的概率。
- 整体更像产品而不是单仓库内部文档。`README.md`、setup 文档、hook 和命令层一起构成了一套完整分发面。

## `agent-skills-main` 的劣势

- 内部文档存在轻微不一致。`references/agent-skills-main/README.md` 写的是 “All 19 Skills”，但实际还有 `using-agent-skills` 这个元 skill；`references/agent-skills-main/AGENTS.md` 的贡献模板与 `docs/skill-anatomy.md` 也不是完全同构。
- 共享 `references/` 的利用率没有想象中高。README 把根级 `references/` 定位为 skills pull in 的参考材料，但很多 skill 仍更多依赖内联内容或 skill 内部资源。
- 生命周期模型更像“通用工程最佳实践包”，对长期、多轮、带审批与回流的状态推进，约束力度不如 AHE。
- 更强调普适性，因此在复杂交付控制上不够“硬”。它能很好地指导流程，但不会强制你用一个统一状态机和一套落盘工件驱动整个任务。

## `ahe-*` 的优势

- 有非常强的 workflow 编排中枢。`skills/ahe-workflow-starter/SKILL.md` 不只是路由器，而是显式定义了 profile、合法节点集合、迁移来源、pause points、回流逻辑和保守决策原则。
- 工件契约和证据链明显强于 `agent-skills-main`。`skills/ahe-test-driven-dev/SKILL.md` 的“实现交接块”、`skills/ahe-regression-gate/SKILL.md` / `skills/ahe-completion-gate/SKILL.md` 的 evidence bundle、`skills/ahe-finalize/SKILL.md` 的 evidence matrix，让每一轮工作都更容易追溯和交接。
- workflow profile 设计很实用。`full` / `standard` / `lightweight` 允许在不降低单节点门禁强度的前提下调整链路密度，这比简单的“要不要用这个 skill”更贴近真实软件交付。
- 支线模型清楚。`skills/ahe-increment/SKILL.md` 与 `skills/ahe-hotfix/SKILL.md` 区分了需求增量和紧急修复，不会把所有“继续改一点”混成一种流转。
- 对“单任务推进”和“fresh evidence”有强约束。`ahe-tasks`、`ahe-tasks-review`、`ahe-test-driven-dev`、`ahe-completion-gate` 都反复强调唯一活跃任务、最新验证、canonical handoff，这是 AHE 的核心竞争力。
- 和仓库设计原则一致。`skills/design_rules.md` 中的 “Markdown-first”“证据优先于印象”“优先单人可维护性”，在 AHE workflow 里都已经被落到了具体规则和记录要求里。

## `ahe-*` 的劣势

- 入口负担偏重。`skills/ahe-workflow-starter/SKILL.md` 承担了太多规则、状态机、profile、迁移和 pause 逻辑，正确读取和正确执行的成本都比较高。
- 家族级公共约定分散在多个 skill 中重复出现。`AGENTS.md` 路径映射、canonical 字段、fresh evidence、回流规则、结论映射等在多个节点重复描述，维护成本高。
- 模板与契约还没有完全统一。`templates/task-progress-template.md` 仍使用 `Current Task` / `Next Action`，而 `skills/ahe-tasks/SKILL.md`、`skills/ahe-tasks-review/SKILL.md`、`skills/ahe-test-driven-dev/SKILL.md`、`skills/ahe-completion-gate/SKILL.md`、`skills/ahe-finalize/SKILL.md` 都要求 `Current Stage`、`Current Active Task`、`Next Action Or Recommended Skill` 等 canonical 字段。
- 可移植性一般。很多 skill 默认假设 `docs/specs/`、`docs/tasks/`、`docs/reviews/`、`docs/verification/`、`RELEASE_NOTES.md`、`task-progress.md` 这些路径存在，跨仓库采用需要额外适配。
- 自动化和无人值守能力受 pause point 影响。规格批准、设计批准和测试设计确认很合理，但会抬高批处理和 autonomous loop 场景的使用门槛。
- AHE 很强，但更像“内部流程语言”而不是“低门槛 skill pack”。这对当前仓库是优点，对外扩散则是阻力。

## 谁更强，取决于目标

- 如果目标是“做一个能被不同 agent / 不同项目快速接入的通用 skill 产品包”，`agent-skills-main` 更强。
- 如果目标是“在一个长期软件交付任务里严格控制阶段、证据、回流和完成定义”，`ahe-*` 更强。
- 如果目标是“把 AHE 打造成更成熟的个人 harness engineering 工作台”，最优路线不是把 AHE 改成 `agent-skills-main`，而是保留 AHE 的强流程骨架，再引入 `agent-skills-main` 式的统一外壳和轻量配套。

## AHE 最值得借鉴的方面

### P0：应该优先做的

| 优先级 | 建议 | 借鉴来源 | 预期收益 |
| --- | --- | --- | --- |
| P0 | 增加一份 AHE 家族级 anatomy 文档，统一 frontmatter、必备章节、handoff 字段、review/gate 结论枚举、模板映射规则 | `references/agent-skills-main/docs/skill-anatomy.md` | 降低跨 skill 漂移，便于后续持续优化 |
| P0 | 对 `ahe-workflow-starter` 做二次瘦身：保留核心路由规则，把示例、矩阵、边界解释继续下沉到 `references/` | `agent-skills-main` 的 progressive disclosure 思路 | 保留状态机强度，同时降低首屏阅读负担 |
| P0 | 统一 `task-progress` canonical schema，并同步更新 `templates/task-progress-template.md` | `agent-skills-main` 的统一 anatomy + AHE 当前字段契约 | 消除真实使用中的字段歧义，减少下游兼容判断 |
| P0 | 为 AHE skill 补齐或统一 `When to Use`、`When NOT to Use`、`Red Flags`、`Verification` 一类固定骨架 | `agent-skills-main` 的 skill anatomy | 提高可扫描性、稳定触发率和一致性 |

### P1：选择性借鉴

| 优先级 | 建议 | 借鉴来源 | 预期收益 |
| --- | --- | --- | --- |
| P1 | 增加更轻量的家族级 meta-skill，例如 `using-ahe-skills`，专门承载全局行为约束、技能发现原则、常见失败模式 | `references/agent-skills-main/skills/using-agent-skills/SKILL.md` | 把一部分全局约定从 starter 中抽离 |
| P1 | 为 AHE 的 code / test / traceability / gate 节点补充 persona 资产 | `references/agent-skills-main/agents/*.md` | 让 review/gate 节点更容易被独立复用或被子代理消费 |
| P1 | 增加薄命令层或命令约定文档，例如 `/ahe-spec`、`/ahe-build`、`/ahe-review` | `references/agent-skills-main/.claude/commands/*.md` | 让常见入口更低摩擦 |
| P1 | 把重复出现的 `fresh evidence`、severity、canonical next action、record path rules 提炼成共享参考文档 | `agent-skills-main` 的 shared references 思路 | 降低跨 skill 重复维护成本 |

### P2：只有在 AHE 准备对外分发时再考虑

| 优先级 | 建议 | 借鉴来源 | 预期收益 |
| --- | --- | --- | --- |
| P2 | 增加 hook / plugin / setup 文档 | `agent-skills-main` 的 `hooks/`、setup docs | 提升外部安装与发现体验 |
| P2 | 增加 repo-agnostic 配置说明，让非 AHE 仓库可以快速映射 `docs/specs/`、`docs/reviews/`、`docs/verification/` 等目录 | `agent-skills-main` 的通用分发思路 | 提高跨仓库复用能力 |
| P2 | 把 AHE workflow 拆成“核心包 + 可选扩展包” | `agent-skills-main` 的产品化思路 | 兼顾轻量使用和全链路使用 |

## 不建议 AHE 直接照搬的方面

- 不建议照搬 `agent-skills-main` 的“更宽的通用工程覆盖”。AHE 的价值不在 skill 数量，而在 workflow 契约和证据链。
- 不建议为了看起来完整而一次性引入 plugin、hooks、commands、agents 全家桶。`skills/design_rules.md` 已明确强调单人可维护性，包装层应该在真实复用需求稳定后再加。
- 不建议削弱 pause points 和 profile-aware gate。它们正是 AHE 区别于普通 skill pack 的核心优势。
- 不建议把 AHE 改成只有建议、没有落盘工件的轻流程。AHE 的 `review / gate / finalize` 价值本来就来自 records and evidence。

## 建议的 AHE 演进路线

### 第一阶段：先做家族一致性修复

- 新增一份 `ahe` 家族级 anatomy 文档。
- 统一 `task-progress` canonical schema。
- 统一各 skill 的固定章节与 verdict 枚举。
- 把重复规则抽到 shared references。

### 第二阶段：再做入口减负

- 精简 `ahe-workflow-starter`。
- 抽出 `using-ahe-skills` 或等价元 skill。
- 让 starter 更像“核心编排器”，让家族公共行为约束从主文件里脱出。

### 第三阶段：最后再做对外化包装

- 命令入口
- persona 资产
- setup / install 文档
- 可选 hook / plugin

## 一句话判断

- `agent-skills-main` 胜在“像产品的 skill pack”。
- `ahe-*` 胜在“像操作系统的 workflow kernel”。
- AHE 最应该借鉴的是 `agent-skills-main` 的统一外壳、统一 anatomy 和低摩擦入口，而不是牺牲自己最强的状态机、证据链和 gate 设计去换取表面上的轻量化。
