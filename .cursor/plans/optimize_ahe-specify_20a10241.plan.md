---
name: optimize ahe-specify
overview: 提升 `ahe-specify` 的需求澄清深度与规格质量控制能力，同时保持 AHE 现有 workflow、工件路径和 `ahe-spec-review` 接口不变。重点是补强澄清轮次、需求结构化表达、质量自检与范围收敛机制。
todos:
  - id: confirm-scheme
    content: 等待你确认这套优化方向与边界，确认是否按此方案改写 `skills/ahe-specify/SKILL.md`
    status: completed
  - id: rewrite-skill
    content: 确认后重构 `skills/ahe-specify/SKILL.md` 的 frontmatter、澄清协议、默认规格结构、自检与重入规则
    status: completed
  - id: validate-fit
    content: 检查改写后内容是否仍与 `ahe-spec-review`、`ahe-workflow-starter` 和 AHE 主链契约兼容
    status: completed
isProject: false
---

# 优化 `ahe-specify` 方案

## 目标

把 `[skills/ahe-specify/SKILL.md](skills/ahe-specify/SKILL.md)` 从“能产出可评审规格草稿”的 skill，提升为“能稳定逼近高质量需求规格”的 skill。

这次优化只改 `ahe-specify` 的澄清与写作方法，不改 AHE 主链契约：

- 仍然必须先经过 `[skills/ahe-workflow-starter/SKILL.md](skills/ahe-workflow-starter/SKILL.md)` 路由
- 仍然输出可提交给 `[skills/ahe-spec-review/SKILL.md](skills/ahe-spec-review/SKILL.md)` 的规格草稿
- 仍然禁止在 `ahe-specify` 阶段发起真人批准
- 仍然保持 `specify -> spec-review -> 真人确认 -> design` 的顺序

## 当前问题

当前 `[skills/ahe-specify/SKILL.md](skills/ahe-specify/SKILL.md)` 已经有正确的门禁意识和最小章节骨架，但仍偏“合格草稿生成器”，主要短板是：

- 澄清维度够用，但缺少更强的提问协议，容易停留在表层需求
- 章节骨架过于最小化，缺少高质量规格常见的结构化支撑，如术语、假设、接口/依赖、需求编号、优先级、边界/负路径
- 验收标准只被要求“存在”，没有要求与功能需求逐条对应、原子化、可验证
- 非功能需求没有展开为设计真正会依赖的类别，容易把关键约束漏到设计阶段才发现
- 对“哪些开放问题可保留、哪些必须先澄清”缺少更可执行的判定规则

## 优化方向

### 1. 把“先澄清”升级为分轮澄清协议

在 `ahe-specify` 中加入明确的澄清轮次，而不只是列出要问哪些主题：

- 第一轮：问题、用户、范围、范围外
- 第二轮：核心行为与关键流程
- 第三轮：异常、边界、失败路径
- 第四轮：约束、依赖、兼容性、外部接口
- 第五轮：非功能需求与验收口径
- 必要时补一轮：术语、假设、待确认项

为什么这么改：

- 现在的 skill 知道“该问什么”，但没有足够强的问法约束
- 分轮澄清可以显著减少“先写后猜”“把开放问题留给后面”的情况

主要参考：

- `[references/longtaskforagent-main/skills/long-task-requirements/SKILL.md](references/longtaskforagent-main/skills/long-task-requirements/SKILL.md)`：它的 CAPTURE -> CHALLENGE -> CLARIFY、多轮按主题提问、场景化追问很强
- `[references/skills-main/skills/doc-coauthoring/SKILL.md](references/skills-main/skills/doc-coauthoring/SKILL.md)`：它把“信息收集”和“文档成型”分层处理，适合借来强化澄清阶段
- `[references/superpowers-main/skills/brainstorming/SKILL.md](references/superpowers-main/skills/brainstorming/SKILL.md)`：它对“范围过大先拆解、不要一上来直接写文档”的约束很有价值

### 2. 把规格最小骨架升级为“高质量但不过度工程化”的默认结构

保留现有最小骨架的简洁性，但增强为更适合高质量澄清的默认模板，例如新增或强化这些部分：

- 背景 / 问题陈述
- 用户角色 / 关键场景
- 术语与定义（按需）
- 功能需求
- 非功能需求
- 外部接口与依赖（按需）
- 约束
- 明确假设（按需）
- 范围外内容
- 验收标准
- 阻塞性开放问题 / 非阻塞开放问题

为什么这么改：

- `ahe-spec-review` 已经在检查边界情况、约束依赖、验收标准，但 `ahe-specify` 的骨架还没有很好地提前承接这些检查项
- 高质量规格不一定要很重，但必须让评审知道“哪些问题已经定了、哪些是故意留白”

主要参考：

- `[skills/ahe-spec-review/SKILL.md](skills/ahe-spec-review/SKILL.md)`：反向约束了 `ahe-specify` 必须提前写清什么
- `[references/longtaskforagent-main/skills/long-task-requirements/SKILL.md](references/longtaskforagent-main/skills/long-task-requirements/SKILL.md)`：它的需求分类（FR/NFR/CON/ASM/IFR/EXC）值得轻量借鉴
- `[references/everything-claude-code-main/skills/product-lens/SKILL.md](references/everything-claude-code-main/skills/product-lens/SKILL.md)`：它的 why / anti-goal / success metric 对“目标、范围外、成功标准”非常有帮助

### 3. 强化“功能需求 + 验收标准”配对规则

将 `ahe-specify` 明确改成：

- 核心功能需求默认逐条编号或至少逐条列项
- 每条核心功能需求都要有至少一个可验证验收标准
- 验收标准优先采用场景化表达，如 Given/When/Then 风格，但不把格式教条化
- 对关键失败路径、边界条件、权限/约束冲突，也要至少落一条验收口径

为什么这么改：

- 当前 skill 要求“核心行为具备验收标准”，但没有要求粒度一致，容易出现一个大段功能描述配一个很泛的验收标准
- 这会直接导致 `ahe-spec-review` 里的“验收标准偏弱或不完整”

主要参考：

- `[references/longtaskforagent-main/skills/long-task-requirements/SKILL.md](references/longtaskforagent-main/skills/long-task-requirements/SKILL.md)`：EARS + Given/When/Then + 每条需求附 acceptance 的组合值得借鉴，但会做 AHE 本地化简化，不直接照搬完整 ISO 流程
- `[skills/ahe-spec-review/SKILL.md](skills/ahe-spec-review/SKILL.md)`：现有评审标准已经要求核心行为具备验收标准

### 4. 明确 NFR、约束、假设、接口的提问与落盘规则

在 `ahe-specify` 中加入“至少检查这些类别是否相关”的 guidance：

- 性能
- 可靠性 / 可恢复性
- 安全 / 权限 / 隐私
- 兼容性 / 迁移影响
- 可观察性 / 运营约束
- 可访问性 / 国际化（有 UI 时）
- 外部系统接口 / 数据契约
- 预算、法规、部署、许可证等外部约束
- 假设及其失效风险

为什么这么改：

- 这些内容常常不是用户主动说出来的，但会直接决定后续设计是否返工
- `ahe-design` 需要这些输入；如果 `ahe-specify` 不主动追问，设计阶段就只能靠猜

主要参考：

- `[references/longtaskforagent-main/skills/long-task-requirements/SKILL.md](references/longtaskforagent-main/skills/long-task-requirements/SKILL.md)`：NFR probes 和 constraints/assumptions/interfaces 的结构非常系统
- `[skills/ahe-design/SKILL.md](skills/ahe-design/SKILL.md)`：下游设计天然依赖这些信息

### 5. 引入“问题分层”与“阻塞性开放问题”规则

在 `ahe-specify` 中明确区分：

- 已确认事项：可直接入规格
- 需用户确认事项：必须先问清再写
- 非阻塞开放问题：可保留在文档中
- 阻塞性开放问题：不得带着它进入 `ahe-spec-review`

同时为重入场景补强规则：

- 若从 `ahe-spec-review` 返回，只围绕 review findings 修订
- 优先处理 `critical` / `important`
- 不重启整轮探索，避免把规格修订退化成“再聊一遍需求”

为什么这么改：

- 当前 skill 已有重入意识，但还缺少更明确的“哪些问题可留、哪些不能留”的操作性
- 这能显著减少 review 循环中的无效往返

主要参考：

- `[skills/ahe-spec-review/SKILL.md](skills/ahe-spec-review/SKILL.md)`：已经定义了 `critical` / `important` / `minor`
- `[references/skills-main/skills/doc-coauthoring/SKILL.md](references/skills-main/skills/doc-coauthoring/SKILL.md)`：迭代修订时强调只补真实缺口，不重做整个文档

### 6. 加入“高质量规格自检表”，而不把 `ahe-spec-review` 内联复制过来

在 `ahe-specify` 的交付前检查中增加更强的自检，但保持它仍然只是草稿产出 skill，不吞掉 review 职责。自检可以覆盖：

- 范围是否明确，范围外是否显式
- 关键功能是否可观察、可验证
- 关键异常 / 边界 / 失败路径是否至少被识别
- 模糊词是否量化或删除
- 是否混入了设计决定
- 非功能需求是否只写“好/快/稳定”而没有度量
- 是否仍有阻塞性开放问题
- 是否足以让设计阶段不靠猜测继续

为什么这么改：

- 目标不是让 `ahe-specify` 替代 `ahe-spec-review`，而是减少低质量草稿流入 review 的概率
- 这会提升整个链路效率，而不是只提升单个 skill 的“字数”

主要参考：

- `[skills/ahe-spec-review/SKILL.md](skills/ahe-spec-review/SKILL.md)`：它的检查清单应反向前置为自检输入
- `[references/longtaskforagent-main/skills/long-task-requirements/SKILL.md](references/longtaskforagent-main/skills/long-task-requirements/SKILL.md)`：8 项质量属性、反模式检测非常适合做轻量化版本

### 7. 收紧 skill frontmatter 的 description，让触发更准

把 `[skills/ahe-specify/SKILL.md](skills/ahe-specify/SKILL.md)` 的 `description` 从“做什么 + 流程说明”收敛成更纯粹的触发条件表达，减少模型只看 description 不读正文的风险。

为什么这么改：

- 当前 description 对人类友好，但对 skill 触发和正文加载不一定最优
- 高质量 skill 不只是正文强，frontmatter 也要能触发正确

主要参考：

- `[references/superpowers-main/skills/writing-skills/SKILL.md](references/superpowers-main/skills/writing-skills/SKILL.md)`
- `[d:\github-harness-engineering\.cursor\skills\skill-creator\SKILL.md](d:\github-harness-engineering\.cursor\skills\skill-creator\SKILL.md)`

## 明确不做的事

- 不把 `ahe-specify` 变成 `ahe-spec-review`
- 不在规格阶段引入具体架构方案、技术选型、类/表/API 设计
- 不照搬 gstack 的 preamble、遥测、品牌化口吻或工具绑定逻辑
- 不把 `ahe-specify` 写成超长大而全文档；必要的重参考内容更适合后续拆到 `references/` 或模板

## 计划中的实际改动

确认后，我会对 `[skills/ahe-specify/SKILL.md](skills/ahe-specify/SKILL.md)` 做一轮聚焦重构，预计包括：

- 重写 `description`
- 重构“工作流”部分为更强的分轮澄清协议
- 升级默认规格结构
- 增加需求粒度与验收标准配对规则
- 增加 NFR / 约束 / 假设 / 接口探测规则
- 增加开放问题分层与 review-return 修订协议
- 增加高质量规格自检表
- 保持现有 handoff、路径、状态、`task-progress.md`、`ahe-spec-review` 接口不变

## 预期效果

优化后的 `ahe-specify` 应该具备这些特征：

- 更少依赖用户一次性说清所有东西
- 更能主动逼出范围边界、反例、失败路径和非功能要求
- 输出的规格更容易一次通过 `ahe-spec-review`，或者至少让 review 的修订意见更聚焦
- 给 `ahe-design` 的输入更稳定，减少“设计阶段才发现需求不完整”的返工

