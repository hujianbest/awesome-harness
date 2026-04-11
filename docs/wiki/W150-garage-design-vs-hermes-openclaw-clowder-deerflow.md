# W150: Garage Design Vs Hermes, OpenClaw, Clowder AI, and DeerFlow

- Wiki ID: `W150`
- 状态: 参考
- 日期: 2026-04-11
- 定位: 记录 `Garage` 当前 `docs` 主线设计与 `Hermes`、`OpenClaw`、`Clowder AI`、`DeerFlow` 的结构对比，帮助后续实现阶段判断哪些能力值得吸收、哪些实现形态不应直接照抄；默认作为参考资料，不作为当前主线真相源。
- 关联文档:
  - `docs/README.md`
  - `docs/GARAGE.md`
  - `docs/architecture/A110-garage-extensible-architecture.md`
  - `docs/architecture/A140-garage-system-architecture.md`
  - `docs/architecture/A150-garage-vision-and-governance-architecture.md`
  - `docs/architecture/A160-garage-pack-platform-architecture.md`
  - `docs/architecture/A170-garage-cross-pack-bridge-architecture.md`
  - `docs/wiki/W010-clowder-ai-harness-engineering-analysis.md`
  - `docs/wiki/W030-hermes-agent-harness-engineering-analysis.md`

这份对比不想回答“谁功能更多”或“谁现在更成熟”，而是回答另一个更关键的问题：

**如果把 `Garage` 当前 `docs` 主线与 `Hermes`、`OpenClaw`、`Clowder AI`、`DeerFlow` 放在一起看，`Garage` 到底想成为什么系统，又刻意不想成为什么系统。**

说明：

- `Garage` 部分以当前主线文档 `A110 / A140 / A150 / A160 / A170` 为准。
- `Hermes` 与 `Clowder AI` 部分主要基于本仓库已有分析文档 `W030` 与 `W010`。
- `OpenClaw` 与 `DeerFlow` 部分主要基于其公开 GitHub README 与公开文档入口信息做结构级比较，不等于完整源码审计。
- 本文比较的是**架构意图与主线设计**，不是代码完成度排行榜。

---

## 一、结论先行

如果把五者压成一句话，当前最重要的判断是：

- `Garage` 不是“另一个聊天壳”，也不是“另一个长任务执行器”，而是在文档层面先冻结一个 `workspace-first`、`governance-bounded`、`self-evolving` 的长期 team runtime。
- 在连续性与长期 runtime 主体这件事上，`Garage` 最接近 `Hermes`。
- 在平台控制面、治理工件化和“团队先于工具”这件事上，`Garage` 最接近 `Clowder AI`。
- 在多入口、local-first、gateway/host 边界和 skills 作为产品能力面这件事上，`Garage` 与 `OpenClaw` 有明显交集，但目标不是做一个多渠道个人助理产品。
- 在长任务执行、sub-agents、skills、sandbox execution 这件事上，`Garage` 与 `DeerFlow` 有明显交集，但当前主线更强调先冻结平台语义与治理边界，再展开执行 harness。

真正让 `Garage` 与这四个项目拉开距离的，不是“多了几个功能名词”，而是下面这组组合判断被同时写成了上游架构约束：

1. `extension` 与 `growth` 是两条并列主线，不是一条主线里的附属能力。
2. `workspace-first` 和 `evidence-first` 不是实现偏好，而是系统真相模型。
3. `GrowthProposal` 是显式治理对象，长期更新要走 `Evidence -> Proposal -> Governance -> Update`。
4. `VisionAndGovernance`、`Pack Platform`、`Cross-Pack Bridge` 都被单独提升为 architecture seam。
5. `docs` 被当作唯一设计真相源，意味着当前主线先冻结边界，再允许实现逐步追上。

这也意味着：**在设计显式性上，当前 `Garage docs` 比这四个项目中的大多数更“先讲清边界”；但在运行时成熟度上，当前 `Garage` 还明显落后于这些已经有较强实现表面的项目。**

## 二、先把五者压成一句话

| 项目 | 如果压成一句话，它更像什么 |
| --- | --- |
| `Garage` | 一个 `docs-first`、`workspace-first`、`governance-bounded`、`self-evolving` 的 creator/team runtime 蓝图。 |
| `Hermes` | 一个长期在线、跨入口、可积累 `memory / session / skill` 的 personal agent runtime。 |
| `OpenClaw` | 一个 local-first、多渠道接入、带 gateway control plane 与 skills 平台的个人助理产品运行时。 |
| `Clowder AI` | 一个把身份、协作、纪律、审计、共享契约和多模型/多 agent 协作工程化的平台控制面。 |
| `DeerFlow` | 一个围绕长任务、sub-agents、skills、memory 与 sandbox execution 组织起来的 super agent harness。 |

这张表最值得注意的地方是：

- `Hermes` 更像长期 agent 本体。
- `OpenClaw` 更像产品化的多入口 agent 外壳与 gateway。
- `Clowder AI` 更像团队协作平台控制面。
- `DeerFlow` 更像长任务执行 harness。
- `Garage` 想做的是把这些方向里对自己有价值的部分吸收后，重新落到一套更强调 `workspace truth + governance + pack seams + self-evolution` 的主线里。

## 三、按维度看主要差异

| 维度 | `Garage` | `Hermes` | `OpenClaw` | `Clowder AI` | `DeerFlow` |
| --- | --- | --- | --- | --- | --- |
| 系统定位 | creator/team runtime + self-evolving control plane | long-lived personal agent runtime | local-first multi-channel assistant runtime | team collaboration / platform control plane | long-task super agent harness |
| 主协作单位 | `team / session / role / pack` | 单一长期 agent 为主 | agent + isolated sessions/agents | agent team + thread/workflow/platform objects | lead agent + sub-agents |
| 主事实面 | `workspace surfaces + evidence + docs artifacts` | runtime state + session store + skills | gateway sessions + workspace + skills | platform services + shared packages + governance docs | gateway/langgraph state + sandbox fs + memory |
| 长期连续性模型 | `memory / session / skill / evidence` 强分层 | `memory / session / skill` 强分层 | sessions + skills + workspace，但没有同等明确的 `evidence/proposal` 主链 | identity / memory / thread / audit 持续存在 | session summarization + long-term memory + filesystem |
| 成长机制 | `Evidence -> Proposal -> Governance -> Update` | self-improving，偏 runtime 内建，但治理对象不如 `Garage` 显式 | skills 搜索/安装、session continuity，更像能力扩展而非显式自演化主链 | 治理演化和流程纪律很强，但不是同一条 proposal-driven self-update 主链 | memory + skills + sub-agents 很强，但不是 governance-first growth loop |
| 扩展方式 | `Shared Contracts + Pack Registry + Capability Packs + Binding` | tool registry + toolsets + skills | gateway tools + skills + multi-agent routing | shared packages + registry + MCP + platform APIs | skills + MCP + Python tools + LangGraph runtime |
| 治理方式 | `VisionAndGovernance` 单独成层，`approval / archive / policy plane` 明确 | `approval / safety` 是运行时协议 | pairing、allowlist、sandbox、gateway security 更强 | `VISION / SOP / feature / audit` 直接参与平台纪律 | sandbox 与配置治理更强，政策平面较弱 |
| 跨能力协作 | `Cross-Pack Bridge` 被正式定义成 architecture seam | delegate/sub-agent 存在，但不是 pack bridge 架构 | session-to-session / agent routing 更强，不是 pack bridge | workflow/handoff 存在，但不是单独的 pack-neutral bridge 架构 | sub-agent orchestration 更强，不是 pack bridge |
| 当前形态 | 设计显式、实现待追赶 | 运行时强、实现偏 monolith | 产品化强、渠道和宿主面很完整 | 平台化强、服务控制面很重 | 执行 harness 强、框架依赖更明显 |

## 四、Garage 与 Hermes 的差异

如果只看“什么最像 `Garage` 的 runtime 脊柱”，`Hermes` 仍然是最接近的参考。

相似处主要有：

- 两者都不是把 agent 当成一次性对话器，而是把它当成长期存在的 runtime 主体。
- 两者都强调多入口共享同一个核心，而不是让不同入口各自长出一套私有逻辑。
- 两者都明确把 `memory / session / skill` 拆开，不接受把全部长期性塞进一个“记忆桶”。
- 两者都承认 approval / safety 不该只是 UI 提醒，而应当是运行时协议的一部分。

但 `Garage` 明显比 `Hermes` 多推进了四层显式化：

1. `Garage` 把 `evidence` 单独提升成主事实与追溯面，而不只把 transcript persistence 当成连续性基础设施。
2. `Garage` 把成长主链冻结成 `Evidence -> Proposal -> Governance -> Update`，而不是只停留在“self-improving / closed learning loop”。
3. `Garage` 把 `Pack Platform` 与 `Cross-Pack Bridge` 明确成平台 seam；`Hermes` 更像统一 agent 本体加工具/技能系统。
4. `Garage` 把治理层提升成 `VisionAndGovernance` 架构，而不是把 approval/safety 主要落在实现协议与 prompt contract 中。

所以更准确的说法不是“`Garage` 像 `Hermes`”，而是：

**`Garage` 更像把 `Hermes` 的长期 runtime 主体，再往上加了一层 docs-first 的治理显式化、pack 平台显式化和成长治理显式化。**

同时，`Hermes` 也提醒了 `Garage` 两个现实问题：

- 一个长期 runtime 很容易在实现上长成大单体，这件事不能只靠文档避免。
- 如果工具、入口、状态恢复和长期连续性真的做深，运行时复杂度会远高于“做几个 workflow”时的直觉。

## 五、Garage 与 OpenClaw 的差异

`OpenClaw` 和 `Garage` 的相似点，主要不在“它也有 skills”，而在下面几件事：

- 都承认 agent 应该跨多个入口持续存在。
- 都偏向 local-first 运行与强宿主控制边界。
- 都把 session、workspace、skills、tooling 看成产品运行面的稳定组成部分。
- 都把 control plane 从“单次聊天”里抬了出来。

但两者的核心目标并不相同。

`OpenClaw` 更像：

- 一个已经强产品化的个人助理 runtime；
- 一个围绕 gateway、多渠道接入、pairing/security、设备节点和 control UI 打磨过的系统；
- 一个把 session isolation、多 agent routing、skills 安装和 host/device capability 暴露给最终用户的产品面。

而 `Garage` 当前 docs 更像：

- 一个先从 `creator/team runtime` 角度冻结平台边界的架构主线；
- 一个把 `workspace truth`、`evidence`、`growth proposal`、`pack platform` 和 `cross-pack bridge` 先写成上游语义的系统；
- 一个更关注“团队如何持续变强”和“不同能力如何在平台边界内协作”的设计，而不是先铺多渠道产品面。

所以：

- 如果后续实现 `host adapter / bootstrap / entry surface`，`OpenClaw` 很值得参考。
- 如果后续实现 `pairing / allowlist / sandbox mode / session isolation`，`OpenClaw` 也很有参考价值。
- 但 `Garage` 不该直接照抄 `OpenClaw` 的渠道广度、产品壳层和 assistant-product 叙事，因为那会把主线从“团队成长 runtime”拉回“多入口个人助理产品”。

## 六、Garage 与 Clowder AI 的差异

如果只看“团队先于工具”“治理不是附属品”“平台层必须被单独命名出来”这些判断，`Clowder AI` 是当前最接近 `Garage` 的另一个极点。

两者的共同点非常强：

- 都不把系统理解成“模型 + prompt + 几个工具”的组合。
- 都承认平台控制面必须存在，而且这个控制面会持有身份、协作、纪律、审计或共享语义。
- 都重视 `vision / SOP / feature / roadmap / decisions` 这类工件，而不是只靠代码约定维持秩序。
- 都把共享契约和 registry 看成平台能力，而不是顺手写在某个实现包里的辅助层。

但 `Garage` 和 `Clowder AI` 还是有几个本质差异：

1. `Clowder AI` 更像一个已经在往团队级服务控制面收束的平台；`Garage` 当前主线仍然选择 `local-first`、`workspace-first` 的 modular runtime。
2. `Clowder AI` 更强调“协作平台已经存在并在运营”；`Garage` 更强调“先冻结平台和治理边界，再允许实现逐步追上”。
3. `Clowder AI` 虽然治理很强，但 `Garage` 把 `growth` 这件事又额外推进了一步，要求它必须成为 `proposal-driven` 的主链。
4. `Garage` 额外把 `Pack Platform` 与 `Cross-Pack Bridge` 拆成独立 architecture seam；这让能力扩展和跨能力交接都变成了正式平台问题，而不只是运行时协调问题。

因此可以把两者的关系理解成：

- `Clowder AI` 更像“治理和协作平台化”的强参考；
- `Garage` 更像“把平台化、治理化、pack 化、growth 化这几件事同时写成一套更强约束的本地主线”。

如果后续要实现 `shared contracts / registry / governance artifacts / control plane vocabulary`，`Clowder AI` 仍然是优先级很高的参考源。

## 七、Garage 与 DeerFlow 的差异

`DeerFlow` 和 `Garage` 的交集，主要在“系统不只回答问题，而要执行长任务”这件事上。

`DeerFlow` 的强项非常明确：

- 它直接把自己定义成 `super agent harness`。
- 它把 `sub-agents`、`memory`、`sandbox`、`skills` 和 filesystem execution environment 组合成一个面向复杂任务的执行框架。
- 它在执行面上已经显式处理了 `LangGraph runtime / Gateway mode / sandbox mode / long-term memory / progressive skill loading` 这些现实问题。

但这和 `Garage` 当前 docs 的中心仍然不一样。

`Garage` 当前主线更关心的是：

- `session / governance / evidence / packs / bridge / growth` 的长期稳定语义；
- 如何让不同能力在统一平台边界内协作；
- 如何让团队从真实工作中形成长期可治理的更新；
- 如何让 `docs` 先成为上游真相，再决定实现层选什么 execution harness。

换句话说：

- `DeerFlow` 更像“执行能力非常强的 harness”；
- `Garage` 更像“先冻结什么样的系统才值得长期演化，然后再决定 execution harness 怎么挂上去”。

这也说明 `DeerFlow` 对 `Garage` 的最大价值，不是直接提供整套平台答案，而是给下面这些实现面提供强参考：

- `sub-agent orchestration`
- `sandbox provider`
- `thread/session filesystem layout`
- `skill progressive loading`
- `tool + MCP + long-task execution` 的现实权衡

但 `Garage` 不应把 `LangGraph`、`Gateway mode` 或某个具体 harness 框架直接提升成平台真相源；否则会让当前主线从“平台语义优先”滑回“实现框架优先”。

## 八、Garage 当前最独特的地方

如果必须总结 `Garage` 当前 docs 和这四个项目的最大区别，我会把它压缩成下面 6 条：

1. `Garage` 把 `docs` 当成唯一设计真相源，因此当前最成熟的是边界定义，不是实现表面。
2. `Garage` 同时把“扩展新能力”和“团队从经验中成长”定义成平台主线，而不是只选其中一条。
3. `Garage` 对成长的要求更严格：必须先有 `evidence`，再有 `proposal`，再进入治理和长期更新。
4. `Garage` 把 `workspace-first` 提升成主事实面，这比“本地存储一下状态”更强。
5. `Garage` 把 `Pack Platform` 和 `Cross-Pack Bridge` 明确成长期 seam，这让能力接入和跨能力交接都能成为稳定平台问题。
6. `Garage` 把 `VisionAndGovernance` 单独成层，这意味着愿景、规则、审批、archive 和成长审查都不是附属能力。

从这个角度看，`Garage` 既不是 `Hermes` 的翻版，也不是 `OpenClaw`、`Clowder AI` 或 `DeerFlow` 的拼装版。

更准确的说法是：

**`Garage` 想吸收 `Hermes` 的长期 runtime 主体、`Clowder AI` 的平台治理视角、`OpenClaw` 的多入口/宿主控制经验、`DeerFlow` 的执行 harness 经验，然后把它们重新收束到一套以 `workspace truth`、`governance`、`pack seams` 和 `self-evolution` 为核心的长期系统里。**

## 九、对后续实现最有价值的参考映射

如果后续实现要继续往下推，最有价值的参考映射大致可以这样看：

| 未来实现面 | 优先参考 |
| --- | --- |
| 长期 runtime 主体、连续性分层、approval 协议 | `Hermes` |
| 治理工件、平台控制面、共享契约层、团队协作纪律 | `Clowder AI` |
| 多入口 host/gateway、session isolation、pairing、安全边界、skills 产品面 | `OpenClaw` |
| sub-agent orchestration、sandbox execution、long-task harness、skill progressive loading | `DeerFlow` |

也就是说，当前最合理的外部吸收方式不是“选一个项目做模板”，而是：

- 用 `Hermes` 校准 runtime 主体；
- 用 `Clowder AI` 校准平台与治理；
- 用 `OpenClaw` 校准多入口与宿主边界；
- 用 `DeerFlow` 校准执行 harness；
- 再回到 `Garage` 自己已经冻结的 `A110 / A140 / A150 / A160 / A170` 主线，判断哪些部分应真正进入实现。

这也是为什么 `Garage` 当前 docs 看起来比一般参考项目“更像设计文档系统”：

- 因为它当前确实优先在冻结上游边界；
- 而不是急着在没有边界的情况下做一个看起来已经很强的 agent 产品或 harness。
