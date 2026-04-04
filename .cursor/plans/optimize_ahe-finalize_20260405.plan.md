---
name: optimize ahe-finalize
overview: 提升 `ahe-finalize` 的收尾门禁、集成边界与证据纪律，重点补强 hard gate、integration 说明、idempotency 和完成前验证要求，同时保持现有输出格式和 AHE 主链收尾定位不变。
---

# 优化 `ahe-finalize` 方案

## 目标

把 `skills/ahe-finalize/SKILL.md` 从“收尾说明 skill”提升为“有硬门禁、可重复执行、证据清晰的收尾 skill”，确保每次结束一个 AHE 工作周期时都能留下可恢复的项目状态。

## 当前短板

- 只有前置条件，没有更强的 hard gate 表述，压力下容易把它当成可提前进入的整理步骤。
- 缺少明确的 integration 视角：谁会把会话带到这里、它读取哪些工件、写回哪些工件。
- 没有显式说明 idempotency，重跑收尾时容易担心覆盖或遗漏。
- 虽然要求记录证据位置，但缺少“必须基于当前最新 completion gate 证据”的强调。

## 优化方向

### 1. 收紧 frontmatter description

把 description 改成更聚焦的触发条件表达，强调“只有在完成门禁已通过、需要沉淀状态和交接时才使用”。

参考：

- `references/superpowers-main/skills/verification-before-completion/SKILL.md`
- `references/superpowers-main/skills/finishing-a-development-branch/SKILL.md`

### 2. 增加 hard gate

明确：

- 只有在 `ahe-completion-gate` 已通过后才能进入
- 如果完成门禁状态不清楚，应先回到 `ahe-workflow-starter`
- 收尾阶段不得混入新的实现工作

参考：

- `references/longtaskforagent-main/skills/long-task-finalize/SKILL.md`

### 3. 增加 integration 说明

显式写清：

- 通常由谁把会话带到这里
- 需要读取哪些工件
- 需要更新哪些工件
- 收尾完成后如何回到下一轮 workflow

参考：

- `references/longtaskforagent-main/skills/long-task-finalize/SKILL.md`

### 4. 增加 idempotency 与证据新鲜度

说明：

- 这个 skill 可以重复执行
- 重跑时优先更新而不是重复制造状态漂移
- 只能引用当前最新 completion gate / regression / review 证据，而不是旧结果

参考：

- `references/superpowers-main/skills/verification-before-completion/SKILL.md`

## 明确不做

- 不把 `ahe-finalize` 变成新的 gate
- 不在这里加入新的实现、修复或 review 动作
- 不改变现有输出格式结构

## 计划中的实际改动

- 收紧 description
- 增加 hard gate
- 增加 integration 与 idempotency
- 在工作流中补强证据新鲜度要求
- 保持输出格式和完成定义不变

## 预期效果

- 更不容易在 completion gate 之前误用 `ahe-finalize`
- 更清楚它与 `ahe-completion-gate`、`task-progress.md`、`RELEASE_NOTES.md` 的关系
- 让重复收尾或跨会话收尾更稳定
