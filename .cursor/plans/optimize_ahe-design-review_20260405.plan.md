# 优化 `ahe-design-review` 方案

## 目标

把 `skills/ahe-design-review/SKILL.md` 从“能判断设计能否进入任务规划”的 skill，提升为“能稳定产出高质量设计评审结果，并为真人确认与后续任务规划提供高质量依据”的 skill。

本次优化不改变 AHE 主链契约：

- 仍然只评审设计，不写任务和代码
- 仍然通过 `通过 | 需修改 | 阻塞` 三态给出结论
- 仍然在 `通过` 后进入设计真人确认，而不是直接进入 `ahe-tasks`
- 仍然在 `需修改` / `阻塞` 时回到 `ahe-design`

## 当前问题

当前 `ahe-design-review` 已具备正确门禁与基础检查清单，但仍偏“合格评审器”，主要短板是：

- 检查清单是对的，但缺少更强的评分标尺，反馈深度不稳定
- 对“需求覆盖”的判断还偏口头，缺少追溯视角
- 对“方案是否真的经过权衡”的审计不够，容易接受只有结论没有代价的设计
- 对“是否已足够支撑任务规划”的判断偏抽象，缺少更具操作性的检查
- 缺少对设计风险、隐藏假设和单点评审盲区的主动挑战方式
- 与 `templates/review-record-template.md` 的结论词存在映射关系，但当前 skill 没有明确提示

## 优化方向

### 1. 增加多维评分标尺

在保持现有 verdict 不变的前提下，加入内部评分维度，例如：

- 需求覆盖
- 架构一致性
- 决策质量
- 接口准备度
- 测试 / 任务规划准备度

为什么这么改：

- 评分标尺能逼迫评审更具体，不会只停留在“有/没有”
- 更适合给后续真人确认提供高质量判断依据

主要参考：

- `references/gstack-main/plan-design-review/SKILL.md`
- `docs/skills_refer.md` 中对 `plan-design-review` 的总结

### 2. 强化需求追溯检查

把“设计是否覆盖需求”升级为明确检查：

- 关键需求能否回指到模块、流程或接口
- 是否存在被设计文档新引入、却无法追溯到已批准规格的内容

为什么这么改：

- 高质量设计评审不能只看“像不像覆盖了”，而要看能不能追溯
- 这能避免设计 quietly 扩 scope，并把新内容一路带进 `ahe-tasks`

主要参考：

- `skills/ahe-design/SKILL.md`
- `skills/ahe-tasks/SKILL.md`

### 3. 增加决策审计

评审时不只看“选定方案写没写”，还要看：

- 是否比较了至少两个候选方案
- 是否说明为什么选定当前方案
- 是否记录了主要收益、代价、风险与缓解思路

为什么这么改：

- 设计质量的核心不只是结构图，而是关键决策是否站得住
- 没有决策审计，评审容易退化成看文档完整性

主要参考：

- `references/everything-claude-code-main/skills/architecture-decision-records/SKILL.md`
- `skills/ahe-design/SKILL.md`

### 4. 强化“任务规划准备度”定义

把当前的“可进入任务规划”细化为：

- 关键接口是否已足够明确
- 模块边界是否足够稳定
- 是否还存在会直接破坏任务拆解顺序的设计空洞
- 测试策略是否足够支持后续任务设计

为什么这么改：

- `ahe-design-review` 的价值就在于防止 `ahe-tasks` 变成猜测
- 如果不把“ready for tasks”写具体，结论就会很主观

主要参考：

- `skills/ahe-tasks/SKILL.md`
- `skills/ahe-design/SKILL.md`

### 5. 增加挑战式评审问题

在正式给 verdict 前，要求主动问自己几类挑战问题：

- 哪个假设一旦不成立，当前设计就会失效
- 哪个模块 / 流程写得像“已设计”，其实仍然靠实现阶段补脑
- 哪个新增行为无法追溯到已批准规格
- 哪个风险如果不在现在指出，最可能在 `ahe-tasks` 或实现阶段爆炸

为什么这么改：

- 高质量评审不是 checklist 打勾，而是主动找隐患

主要参考：

- `references/everything-claude-code-main/skills/santa-method/SKILL.md`
- `references/gstack-main/plan-design-review/SKILL.md`

### 6. 明确结论词与模板字段映射

在使用 `templates/review-record-template.md` 时，补充说明：

- `通过` 对应 `pass`
- `需修改` 对应 `revise`
- `阻塞` 对应 `blocked`

为什么这么改：

- 当前模板和 skill 的结论词不同，但本质兼容
- 显式写出来能减少落盘时的歧义

主要参考：

- `templates/review-record-template.md`
- `skills/ahe-design-review/SKILL.md`

## 明确不做的事

- 不把 `ahe-design-review` 变成 `ahe-design`
- 不在评审阶段开始写任务、伪代码或修复方案实现
- 不引入与 `ahe-workflow-starter` 冲突的新的 verdict 或新的流程节点

## 计划中的实际改动

会对 `skills/ahe-design-review/SKILL.md` 做一轮聚焦重构，预计包括：

- 收紧 `description`
- 增加高质量设计评审基线
- 强化证据读取与评审方法
- 增加多维评分标尺
- 强化需求追溯、决策审计、接口准备度与任务规划准备度检查
- 增加挑战式评审问题
- 明确模板字段映射与落盘说明

## 预期效果

优化后的 `ahe-design-review` 应该具备这些特征：

- 不只是判断“设计文档像不像完整”，而是判断它是否真的能支撑进入任务规划
- 反馈更有层次，能更快指出高风险设计空洞
- 输出更适合作为真人确认前的高质量评审依据
- 更能防止设计 quietly 扩 scope 或把风险拖到 `ahe-tasks`
