# 优化 `ahe-tasks-review` 方案

## 目标

把 `skills/ahe-tasks-review/SKILL.md` 从“能判断任务计划是否大致可用”的 skill，提升为“能稳定判断任务计划是否已经真正具备执行准备度”的 skill。

本次优化不改变 AHE 主链契约：

- 仍然通过 `通过 | 需修改 | 阻塞` 三态给出结论
- 仍然在 `通过` 后进入 `ahe-test-driven-dev`
- 仍然在 `需修改` / `阻塞` 时回到 `ahe-tasks`
- 仍然必须把结论写入仓库中的 review 记录工件

## 当前问题

当前 `ahe-tasks-review` 已具备正确门禁和基础检查清单，但仍偏“轻量检查器”，主要短板是：

- 检查项没有对齐 `ahe-tasks` 已经要求的高质量任务计划结构
- 缺少证据优先的预读顺序，容易凭印象判断
- 对“验证准备度”仍偏抽象，缺少更可执行的门槛
- 对依赖、关键路径、单任务推进风险的检查不够具体
- 输出格式有 severity 占位，但缺少更清晰的严重度与修复导向
- 与通用 review 模板的英文 verdict 字段映射没有明确说明

## 优化方向

### 1. 把 `ahe-tasks` 的高质量结构映射进 review 检查

评审不只看粒度 / 顺序 / 验证 / 追溯四大项，还要显式检查：

- 文件 / 工件影响图
- 需求与设计追溯
- 任务单元字段是否完整
- 当前活跃任务选择规则
- 首个活跃任务或高风险任务的测试设计种子

为什么这么改：

- review skill 必须真正 gate 住 upstream skill 的产物契约

主要参考：

- `skills/ahe-tasks/SKILL.md`
- `skills/ahe-tasks-review/SKILL.md`

### 2. 增加证据优先的预读顺序

要求在 verdict 前，先读：

- `AGENTS.md`
- 任务计划
- `task-progress.md`（如存在）
- 必要时回查规格 / 设计锚点

为什么这么改：

- 任务计划评审本质上是执行门禁，不能只靠聊天记忆

主要参考：

- `skills/ahe-workflow-router/SKILL.md`
- `references/longtaskforagent-main/skills/long-task-work/SKILL.md`

### 3. 强化“可执行验证”门槛

把“有验证方式”提升为：

- 关键任务是否给出明确验证入口
- 是否说明预期证据或预期结果
- 是否仍存在“做完再看”的模糊任务

为什么这么改：

- 高质量任务计划 review 要判断能否冷启动执行，而不只是“看起来合理”

主要参考：

- `references/superpowers-main/skills/writing-plans/SKILL.md`
- `references/superpowers-main/skills/executing-plans/SKILL.md`

### 4. 增加依赖与关键路径检查

显式检查：

- 是否存在遗漏依赖
- 是否存在顺序错误
- 是否存在会导致并行冲突的任务切分

为什么这么改：

- 任务计划的核心风险之一就是顺序和依赖假设错误

主要参考：

- `references/everything-claude-code-main/skills/blueprint/SKILL.md`
- `references/everything-claude-code-main/skills/ralphinho-rfc-pipeline/SKILL.md`

### 5. 强化 findings 的严重度和修复导向

要求 findings 不只是指出问题，还要说明：

- 为什么会阻塞实现
- 这是 `需修改` 还是 `阻塞` 级别的问题
- 修订方向应落在哪一类补强上

为什么这么改：

- 高质量 review 结果应该让 `ahe-tasks` 下一轮修订更聚焦

主要参考：

- `references/gstack-main/plan-eng-review/SKILL.md`
- `skills/ahe-design-review/SKILL.md`

### 6. 明确 review 模板 verdict 映射

补充说明：

- `通过` -> `pass`
- `需修改` -> `revise`
- `阻塞` -> `blocked`

为什么这么改：

- 当前 template 和 AHE verdict 词不同，但语义兼容

主要参考：

- `skills/templates/review-record-template.md`
- `skills/ahe-tasks-review/SKILL.md`

## 明确不做的事

- 不把 `ahe-tasks-review` 变成 `ahe-tasks`
- 不在 review 阶段开始拆新任务或写实现建议
- 不取代 `ahe-test-driven-dev` 的真人测试设计确认门禁

## 计划中的实际改动

会对 `skills/ahe-tasks-review/SKILL.md` 做一轮聚焦重构，预计包括：

- 收紧 `description`
- 增加高质量任务评审基线
- 增加证据预读与评审方法
- 对齐 `ahe-tasks` 新的任务计划契约
- 强化可执行验证、依赖 / 关键路径、测试种子和单任务推进检查
- 强化 severity 与修订导向
- 明确模板 verdict 映射

## 预期效果

优化后的 `ahe-tasks-review` 应该具备这些特征：

- 不只是判断任务计划“像不像能做”，而是判断它是否真的能安全进入实现
- 更容易发现任务过大、依赖错误、验证模糊和追溯缺口
- 更稳定地给 `ahe-test-driven-dev` 一个可执行、可保守恢复的上游输入
