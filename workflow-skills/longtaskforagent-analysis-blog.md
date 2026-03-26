# LongTaskForAgent 技能体系分析：为长周期交付打造一条“可恢复、可验证、可接力”的 Agent 流水线

很多 AI coding workflow 的问题，不是模型不会写代码，而是**任务一长，系统就开始失忆、漂移、偷步骤或者只完成一半**。`longtaskforagent` 这套 skills 的真正野心，就是把这种“长周期任务不可靠”变成一个可工程化处理的问题。它不是单纯地提高 Agent 的聪明程度，而是通过阶段划分、磁盘工件、硬门禁和会话接力，让 Agent 在跨上下文、跨会话、跨多日的工作里仍然尽量保持稳定。

和 `superpowers` 相比，`longtaskforagent` 明显更像一套完整的软件交付流水线。它覆盖从需求澄清、SRS 编写、UCD、设计、ATS、项目初始化、单特性迭代开发、质量门禁、特性验收测试、系统测试，到最终文档收尾的全过程。换句话说，它要解决的不是“这次回答怎么更好”，而是“一个复杂项目如何被 Agent 持续推进直到交付”。

## 一、LongTaskForAgent 的核心设计思想

### 1. 长任务不能只靠上下文，要靠持久化工件

在 `using-long-task` 和 `architecture.md` 里，这套体系反复强调一件事：**长任务一定会超出单次上下文窗口，因此必须靠磁盘上的持久化工件来传递状态。**

这些工件包括：

- `docs/plans/*-srs.md`：定义做什么
- `docs/plans/*-ucd.md`：定义界面与视觉规范
- `docs/plans/*-design.md`：定义怎么做
- `docs/plans/*-ats.md`：定义如何验收
- `feature-list.json`：结构化任务清单与共享状态
- `task-progress.md`：跨会话日志
- `RELEASE_NOTES.md`：用户可见变更记录
- `long-task-guide.md`：项目定制化 worker 指南

这和 OpenAI 在 [Run long horizon tasks with Codex](https://developers.openai.com/cookbook/examples/codex/long_horizon_tasks) 中强调的“durable project memory”几乎是同一种思想。OpenAI 的做法是 `Prompt.md + Plan.md + Implement.md + Documentation.md`；`longtaskforagent` 则把它工程化成更细分的标准工件，并让每个阶段都围绕这些工件运作。

### 2. 不靠“一个大 Agent”，而靠“相位路由 + 子技能编排”

`using-long-task` 做的第一件事不是回答问题，而是检查项目当前状态，然后把会话路由到正确阶段：

- 没有 SRS，就去 `long-task-requirements`
- 有 SRS 没有 UCD，就去 `long-task-ucd`
- 有设计没 ATS，就去 `long-task-ats`
- 有 `feature-list.json` 但还有失败特性，就去 `long-task-work`
- 全部特性通过后，再进入系统测试阶段

这种“相位检测”非常重要。它让系统不会因为用户一句“继续”就模糊地往前冲，而是先问清楚项目卡在哪个阶段。这个思路和 LangChain 的 [Plan-and-Execute](https://blog.langchain.com/plan-and-execute-agents/) 相似，但更严格，因为它不仅区分计划与执行，还进一步把执行拆成多个受控阶段。

### 3. 把软件工程前移，并且前移得非常彻底

`longtaskforagent` 的一个鲜明特点是：**大量团队平时习惯后补的内容，在这里都被前置成硬门槛。**

例如：

- 没有 SRS，不允许设计和编码。
- 没有设计，不允许初始化和特性拆解。
- 没有 ATS，不允许进入初始化。
- 缺配置就不能开始特性工作。
- TDD、覆盖率、变异测试、Feature-ST 任何一个门没过，都不能把特性标记为完成。

这其实是一种非常“重工艺”的设计，但它解决的是长周期项目里最痛的几个问题：需求漂移、设计含糊、测试不成体系、阶段之间缺少追踪关系。对于复杂项目来说，这种重并非浪费，而是让 Agent 输出可累积、可审查、可持续。

## 二、为什么这套体系特别适合长周期任务

如果说很多通用 Agent 框架的默认假设是“任务在一个会话里大致能做完”，那么 `longtaskforagent` 的默认假设恰恰相反：**任务一定跨会话，而且每次重新进入时都不能相信模型还记得。**

所以它做了三件很关键的事。

### 1. 用结构化状态抵抗“会话失忆”

`feature-list.json` 的价值非常大。它不像 Markdown 那样容易被模型随手改坏，而是把特性 ID、优先级、依赖、状态、`srs_trace`、验证步骤等关键状态保持为结构化数据。`architecture.md` 甚至专门解释了为什么不用 Markdown 列表来维护 feature inventory。

这和 Cursor 在 [Expanding our long-running agents research preview](https://www.cursor.com/blog/long-running-agents) 里强调的 harness 思路很一致：长任务之所以能跑得久，不只是模型更强，而是运行时提供了更稳定的计划、状态和验证闭环。

### 2. 用“单特性一周期”控制任务粒度

`long-task-work` 明确规定：**一个 session 只完成一个 feature**，顺序必须是 Orient -> Bootstrap -> Config Gate -> Feature Design -> TDD -> Quality -> Feature-ST -> Persist -> End Session。

这看起来保守，但非常符合长任务的工程现实。Cognition 在 [Introducing Devin](https://cognition.ai/blog/introducing-devin/) 里强调，真正有用的自主软件工程 agent 要能连续做成千上万个决策，同时还要能自我修复。问题在于，决策链一长，局部失误就会放大。所以 `longtaskforagent` 的策略不是追求一次吞下更多，而是通过**单特性闭环**把每次风险压缩在可控范围内。

### 3. 用硬门禁防止“看起来完成了”

这一点是很多工作流里最容易缺失的。`longtaskforagent` 不接受“测试大概过了”“功能应该没问题”“UI 看起来正常”这种表达，它要求：

- TDD 必须先红后绿
- Coverage Gate 必须过阈值
- Mutation Gate 必须过阈值
- Feature-ST 必须生成正式测试文档并执行
- Inline Compliance Check 必须对齐设计、测试清单、依赖版本、UCD token

这套做法和 Anthropic 提到的 evaluator-optimizer 很像，也与 Cursor 长任务实践中的“plan + multiple agents checking each other’s work”一致。不同的是，`longtaskforagent` 把这些校验直接写进了工作流骨架，而不是依赖操作者自觉。

## 三、从行业文章看，它代表了哪种 Agent 方法论

把 `longtaskforagent` 放在今天的 Agent 工程实践里看，它明显属于“**长期任务的流程化 scaffold**”这一派，而不是“一个聪明 Agent 自己搞定一切”这一派。

和 OpenAI 的 long-horizon 经验相比，它的共性是：

- 都强调 durable memory
- 都强调计划、验证、状态文档
- 都把连续执行拆成可检查的里程碑

和 Cursor 的 long-running agents 相比，它的共性是：

- 都承认长任务的关键不是单轮回答质量，而是长时间保持对目标的贴合
- 都强调 planning before execution
- 都强调通过额外结构和检查来降低漂移

和 Devin 这一类自主软件工程系统相比，它的共性是：

- 都把 shell、编辑器、浏览器、测试等真实工具视作必要能力
- 都强调能够持续规划、执行、修复

而它自己的独特之处在于：**它把这些理念压缩成了一套适合日常仓库使用的 skills 套件**。不是论文，不是框架白皮书，而是一套可以直接拿来约束 Agent 行为的工作协议。

## 四、如何高效使用 LongTaskForAgent

如果你希望这套体系真正带来效率，而不是变成流程负担，建议按下面的方式使用。

### 1. 第一次进入项目时，接受“前期会更慢”

`long-task-requirements`、`long-task-ucd`、`long-task-design`、`long-task-ats` 这些步骤会明显拉长前期时间。但如果项目跨度大、参与人多、需求会多次变动，这些前置文档会在后期把时间赚回来。高效使用它的前提，不是跳过前期，而是认可前期文档就是长期效率的一部分。

### 2. 把工件当成“单一事实来源”

真正高效的使用方式，不是每次都重新给 Agent 解释项目，而是让 Agent 读：

- `feature-list.json` 看当前特性状态
- `task-progress.md` 看上次做到哪
- `docs/plans/*.md` 看需求、设计、验收策略
- `long-task-guide.md` 看项目特有命令

一旦这些文件维护得好，下一次会话的冷启动成本就会显著下降。

### 3. 坚持“一次只推进一个 feature”

这条规则看起来慢，实际上很快。因为很多长任务的慢，不是慢在编码，而是慢在“半做半没做”的中间状态过多。`longtaskforagent` 的一大优点，就是强迫每次会话形成一个完整闭环，让项目状态始终可恢复、可接棒。

### 4. 不要试图绕过质量门禁

如果你把 Coverage、Mutation、Feature-ST 看成“可选优化”，这套体系会显得很重；但如果你在做的是跨会话、多阶段、多依赖的真实项目，就会理解这些门禁是在替后续几十轮会话省错。高效使用它，不是想办法绕过去，而是让每个阶段自然产出下阶段所需证据。

### 5. 需求变更和紧急修复要走专门入口

`increment-request.json` 和 `bugfix-request.json` 是很聪明的设计。它们把“需求追加”和“紧急修复”从正常主线里分流出来，避免项目状态被随手改坏。对长项目来说，这种显式入口非常重要，因为最容易破坏交付稳定性的，往往不是原计划本身，而是中途插单。

## 五、它的优势与代价

`longtaskforagent` 的优势很明显：阶段清晰、状态可恢复、验证充分、跨会话稳定性强、特别适合复杂项目和长期交付。

但它的代价也同样明显：文档多、流程重、门禁多、前期成本高。对于一个两小时内就能完成的小改动，这套体系几乎一定过重。它真正适合的是以下场景：

- 项目会持续多天甚至多周
- 需求、设计、测试都需要沉淀成文档
- 希望多个 Agent/多次会话都能接着做
- 对质量证据和交付可审查性要求高

一句话概括：**它不是为了让 Agent 更快地开始写代码，而是为了让 Agent 更可靠地把项目做完。**

## 六、给读者的一个结论

`longtaskforagent` 最值得学习的，不是某个具体 prompt，而是它背后的工程判断：长任务失败，往往不是败在模型不会写一段代码，而是败在没有稳定的阶段结构、没有能跨会话传承的状态、没有足够严格的验证闭环。

OpenAI、Anthropic、Cursor、Cognition 近两年的文章都在从不同角度指向同一个方向：Agent 的上限，不只取决于模型能力，也取决于 harness、memory、planning、verification 和 role design。`longtaskforagent` 做的事情，就是把这些原则落成一个面向软件交付的实际体系。

如果你关心的是“如何让 Agent 处理真正的长周期项目，而不是只在 demo 里表现聪明”，那么这套体系值得认真研究。它不是最轻的方案，但很可能是更接近真实工程现场的方案。

## 参考资料

- OpenAI Cookbook: [Run long horizon tasks with Codex](https://developers.openai.com/cookbook/examples/codex/long_horizon_tasks)
- OpenAI Cookbook: [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans/)
- Anthropic: [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- Anthropic: [Building Effective AI Agents Guide](https://resources.anthropic.com/building-effective-ai-agents)
- LangChain Blog: [Plan-and-Execute Agents](https://blog.langchain.com/plan-and-execute-agents/)
- Cursor Blog: [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)
- Cursor Blog: [Expanding our long-running agents research preview](https://www.cursor.com/blog/long-running-agents)
- Cognition: [Introducing Devin](https://cognition.ai/blog/introducing-devin/)
