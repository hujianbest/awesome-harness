# Superpowers 技能体系分析：把 Agent 变成“会按流程工作的开发搭子”

如果把很多团队对 AI 编程助手的期待浓缩成一句话，大概会是：不只是“能写代码”，而是“能按靠谱的方法做事”。`superpowers` 这套 skills 的价值，恰恰不在于它塞给 Agent 更多技巧，而在于它试图把开发流程显式化、模块化、可复用化。你可以把它理解为一个面向编码 Agent 的“轻量操作系统”: 不同任务进入不同技能，技能之间有严格的调用顺序，输出又能自然衔接到下一步。

从仓库内容看，`superpowers` 的核心不是某一个超级技能，而是一组可以组合的流程单元，例如 `using-superpowers`、`brainstorming`、`writing-plans`、`subagent-driven-development`、`dispatching-parallel-agents`、`test-driven-development`、`finishing-a-development-branch`。这说明它的设计目标不是替用户“替代思考”，而是把“先设计、后计划、再执行、最后收尾”的开发节奏固化下来，让 Agent 少走捷径，也少靠临场发挥。

## 一、Superpowers 的核心设计思想

### 1. 先路由，再行动

`using-superpowers` 最强硬的一条规则是：**只要有 1% 的可能某个 skill 适用，就必须先调用 skill，再进行任何回答或操作。** 这其实是在解决今天 Agent 常见的一个问题: 太快开始干活，太晚进入正确流程。

这种思想和 Anthropic 在 [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents) 里强调的“用简单、可组合的工作流替代大而全的智能幻觉”非常一致。Anthropic 把路由、并行化、orchestrator-workers、evaluator-optimizer 看作高价值模式；`superpowers` 则把这些模式具体落成了仓库内可复用的技能清单。换句话说，它不是在问“模型够不够聪明”，而是在问“什么时候该切到哪个工作流”。

### 2. 过程技能优先于实现技能

在 `superpowers` 里，`brainstorming`、`test-driven-development`、`systematic-debugging` 这一类技能的优先级高于“去写代码”。这是一个非常关键的价值观：**先决定怎么做，再决定做什么。**

比如用户说“帮我做个功能”，直觉上很多 Agent 会直接开始读代码、想实现；但 `brainstorming` 要求先探索上下文、逐步澄清需求、提出多个方案、让用户批准设计、落成 spec，再转入 `writing-plans`。这和 OpenAI 在 [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans/) 中强调的“先形成可执行计划文档，再进入长时间实现”高度同构。

### 3. 把“好习惯”变成硬约束

`superpowers` 最大的优点不是灵活，而是**在关键环节故意不灵活**。例如：

- `test-driven-development` 明确要求先写失败测试，再写最小实现。
- `writing-plans` 要求计划必须精确到文件路径、测试命令、提交粒度。
- `subagent-driven-development` 要求每个任务由独立子代理执行，并经过“规格审查 -> 代码质量审查”两轮关卡。
- `finishing-a-development-branch` 要求测试通过后，才允许进入 merge / PR / 保留分支 / 丢弃工作等后续选项。

这背后的思路很像 evaluator-optimizer: 不是让一个 Agent 一路冲到底，而是在执行链路里放入显式评审点。对于真实软件开发来说，这种“慢一点但更可验证”的设计，比“高自由度自动编程”更接近团队能接受的协作方式。

## 二、为什么说它像“Agent 的开发操作系统”

如果只看单个 skill，`superpowers` 很像一堆 prompt 模板；但把它们串起来看，它更像一个分层系统：

- `using-superpowers` 负责总入口和路由纪律。
- `brainstorming` 负责把模糊想法收敛为可批准的设计。
- `writing-plans` 负责把设计翻译为可执行计划。
- `subagent-driven-development` 和 `dispatching-parallel-agents` 负责执行时的任务调度。
- `test-driven-development`、`systematic-debugging`、`requesting-code-review` 负责局部质量控制。
- `finishing-a-development-branch` 负责交付收尾。

这种设计和 LangChain 的 [Plan-and-Execute](https://blog.langchain.com/plan-and-execute-agents/) 是同一类思路：把“规划”和“执行”拆开，让高层 Agent 决定路径，让底层 Agent 处理局部动作。但 `superpowers` 更进一步的地方在于，它并没有停在抽象架构，而是把每个阶段都变成了带约束、带产物、带交接关系的可落地 skill。

## 三、它最适合解决什么问题

`superpowers` 特别适合三类场景。

第一类是**中等复杂度的软件开发任务**。需求不算巨大，但也不是“一次回复里随手写完”就能稳妥完成的，比如新增一个子系统、调整交互流程、做一个跨文件改动。此时 `brainstorming -> writing-plans -> subagent-driven-development` 的组合能显著降低返工。

第二类是**多人协作、需要留痕的工作**。`writing-plans` 生成文档，`finishing-a-development-branch` 固化收尾动作，意味着整个过程是可审查、可复现、可 handoff 的。

第三类是**容易被 Agent“想当然”搞偏的任务**。例如看似简单，但其实有隐含约束、需要测试策略、需要边界澄清。这类任务最怕“看起来很快做完，实际上从一开始就方向不对”，而 `superpowers` 正是在前置阶段消化这种风险。

## 四、如何高效使用 Superpowers

如果你是第一次上手，不建议把它当成“全自动大招”，而应该按下面的方式使用。

### 1. 有创造性需求时，先走 `brainstorming`

只要任务涉及“新增功能、改行为、做设计”，就优先让 Agent 进入 `brainstorming`。这一步的价值不只是问问题，而是把很多团队平时口头里说不清的约束提前摊出来。真正高效的地方在于：你花的不是额外时间，而是在减少后面的返工时间。

### 2. 设计确认后，强制生成计划

`writing-plans` 非常适合把“讨论结果”转成“执行清单”。如果你的团队已经有 spec 文档、issue 描述或 PRD，这一步尤其值得做，因为它会把抽象需求翻译成具体文件、测试、命令、提交粒度。OpenAI 在 ExecPlan/PLANS.md 里强调计划必须“新手可执行、可验证、可恢复”，`superpowers` 的计划技能本质上是在做同样的事情。

### 3. 多步骤实现优先用 `subagent-driven-development`

这是 `superpowers` 中最有工程味的一部分。它不是让主 Agent 一口气写完，而是让主 Agent 做协调者：

- 拆任务
- 给子代理喂完整上下文
- 让实现子代理完成局部修改
- 先做规格审查，再做代码质量审查
- 问题不过关就回环修复

这套模式非常适合真实开发，因为它把“上下文隔离”和“阶段性评审”都做了。与其说它在追求绝对自动化，不如说它在追求**低漂移的自动化**。

### 4. 只有在真正独立时才并行

`dispatching-parallel-agents` 明确强调，只有任务之间没有共享状态、没有顺序依赖时，才值得并行。这一点和 Anthropic 的 parallelization 模式、以及 Cursor 在 [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents) 里总结的经验非常一致：并行能加速，但协调成本会迅速吞掉收益。`superpowers` 在这里的态度是克制的，这是优点。

### 5. 把 TDD 和 code review 当作默认护栏

`superpowers` 不是“写完再补测试”，而是鼓励你把 TDD、review、branch finishing 都纳入标准轨道。对个人开发者来说，这会显得“流程重”；但对团队使用 Agent 来说，这恰恰是把不稳定输出变成可接受工程产物的关键。

## 五、它的边界与代价

这套体系并不适合所有任务。

如果只是改一个字面量、查一个 API、回答一个概念问题，`superpowers` 会显得过重。它真正发力的地方，是那些“如果现在不加流程，后面一定会补交学费”的任务。

它的另一个代价是前置思考更多、产物更多、回合数更多。你会感觉它不如“直接让模型开写”那么爽快。但这和很多成熟工程实践一样，短期看像负担，长期看是降低不可控性。尤其在代码库越来越大、交付要求越来越高的时候，这种可组合技能体系会比单个万能 prompt 更稳。

## 六、给读者的一个简单结论

如果你把 `superpowers` 只看成“很多 prompt 的集合”，会低估它。更准确的理解是：它在尝试把经验型开发流程沉淀成 Agent 能稳定执行的工作流，把“设计、计划、执行、评审、收尾”这些原本隐含在人类工程师脑中的动作，外化成一套明确的协作协议。

从行业趋势看，这条路是对的。Anthropic 在强调可组合 agent 模式，OpenAI 在强调计划文档和 long-horizon runbook，Cursor 在强调长时任务要有规划、角色分工和校验闭环。`superpowers` 的特别之处，不是提出了全新理论，而是把这些理念做成了日常可用的技能体系。

如果你的目标是“让 Agent 更像一个有工程纪律的搭子，而不是一个随机灵感很强的实习生”，那 `superpowers` 是一套值得认真吸收的方法论。

## 参考资料

- Anthropic: [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- Anthropic: [Building Effective AI Agents Guide](https://resources.anthropic.com/building-effective-ai-agents)
- OpenAI Cookbook: [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans/)
- LangChain Blog: [Plan-and-Execute Agents](https://blog.langchain.com/plan-and-execute-agents/)
- Cursor Blog: [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)
