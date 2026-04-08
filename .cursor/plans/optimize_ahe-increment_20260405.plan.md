# 优化 `ahe-increment` 方案

## 目标

把 `skills/ahe-increment/SKILL.md` 从“能处理变更请求”的 skill，提升为“能稳定做出高质量增量变更分析、显式失效下游批准、同步受影响工件并安全回流主 AHE 链路”的 skill。

本次优化不改变 AHE 主链契约：

- 仍然由 `ahe-workflow-router` 拥有分支进入与恢复编排权
- 仍然不能从变更请求直接跳进实现
- 仍然由 `ahe-specify` / `ahe-design` / `ahe-tasks` 负责各自产物的高质量重写
- 仍然由 `ahe-test-driven-dev` 作为唯一实现入口

## 当前问题

当前 `ahe-increment` 已经要求先做影响分析再更新工件，但仍存在几个影响质量的短板：

- 缺少开局的状态定向，没先固定当前 profile、阶段、活跃任务和已批准工件基线
- 影响分析还偏概念化，缺少更稳定的“变更包 / 影响矩阵 / 失效项”表达
- 没有显式说明哪些旧批准、旧任务、旧验证证据会失效
- 回流到正确阶段时仍然使用自然语言下一步，缺少 canonical `ahe-*` handoff
- 与 `ahe-hotfix` 的边界不够主动，缺少“这到底是范围变化还是实现缺陷”的快速分流
- 缺少对 profile 升级信号和 active task 失效的明确处理

## 优化方向

### 1. 增加开局定向与基线锁定

先固定：

- 当前 workflow profile
- 当前阶段
- 当前活跃任务
- 当前已批准规格 / 设计 / 任务工件
- 当前已实现内容和验证证据（如受影响）

为什么这么改：

- 增量变更的质量，不只取决于“变了什么”，还取决于“原来已经走到哪一步”

主要参考：

- `references/longtaskforagent-main/skills/long-task-increment/SKILL.md`
- `skills/ahe-workflow-router/SKILL.md`

### 2. 引入结构化“变更包 / 影响矩阵”

要求至少显式列出：

- New / Modified / Deprecated 项
- 受影响工件
- 失效的批准 / 任务 / 验证证据
- 需要回退到哪个阶段重新收敛

为什么这么改：

- 这能把“影响分析”从泛泛判断升级成可核对产物
- 也能更稳定地区分“只改规格”与“规格 / 设计 / 任务 / 已实现内容一起受影响”

主要参考：

- `references/longtaskforagent-main/skills/long-task-increment/SKILL.md`
- `references/superpowers-main/skills/writing-plans/SKILL.md`

### 3. 增加批准失效与下游失效规则

要求明确判断：

- 哪些批准不再有效
- 哪些任务计划不再可执行
- 哪些测试设计 / 验证证据已失效
- 当前活跃任务是否必须重选

为什么这么改：

- 变更 skill 的关键价值之一，是阻止旧批准和旧执行上下文被误用

主要参考：

- `skills/ahe-tasks/SKILL.md`
- `skills/ahe-test-driven-dev/SKILL.md`

### 4. 强化 hotfix / increment 边界

增加快速判断：

- 如果是“原本应成立的行为没有成立”，偏向 hotfix
- 如果是“预期、范围、验收改变了”，偏向 increment

为什么这么改：

- 这能减少热修和增量分支互相吞掉对方工作

主要参考：

- `skills/ahe-hotfix/SKILL.md`
- `skills/ahe-workflow-router/SKILL.md`

### 5. 收紧 canonical handoff

要求 `Next Action Or Recommended Skill` 优先写 canonical `ahe-*` skill ID，而不是：

- `重新进入规格评审`
- `回到实现阶段`
- 其它自由文本

为什么这么改：

- router 已经把显式交接做成受控字段，增量 skill 也必须对齐

主要参考：

- `skills/ahe-workflow-router/SKILL.md`
- `skills/ahe-hotfix/SKILL.md`

### 6. 增加 profile 升级信号

当变更引入以下特征时，要求显式记录：

- 新架构决策
- 新接口 / 新约束 / 新 NFR
- 影响面超出当前 profile 预期

为什么这么改：

- `ahe-increment` 不决定 profile，但必须及时把升级信号写出来

主要参考：

- `skills/ahe-workflow-router/SKILL.md`
- `skills/ahe-design/SKILL.md`

### 7. 补强实现回流条件

若分析后允许回到实现阶段，要求明确：

- 当前活跃任务是否仍有效
- 是否必须重新做任务评审
- 是否需要重新做测试设计确认

为什么这么改：

- 否则很容易把变更后的主链继续接到一个已经失效的 active task 上

主要参考：

- `skills/ahe-tasks/SKILL.md`
- `skills/ahe-test-driven-dev/SKILL.md`

## 明确不做的事

- 不把 `ahe-increment` 写成第二个 `ahe-specify`
- 不直接替代 `ahe-design` 或 `ahe-tasks` 完成全部下游重写
- 不在变更 skill 内直接推进实现
- 不抢走 `ahe-workflow-router` 的恢复编排权

## 计划中的实际改动

会对 `skills/ahe-increment/SKILL.md` 做一轮聚焦增强，预计包括：

- 增加开局定向与基线锁定
- 引入结构化变更包 / 影响矩阵
- 增加批准失效、active task 失效与验证失效规则
- 增加 hotfix / increment 分流判断
- 收紧 canonical handoff 与状态同步字段
- 增加 profile 升级信号和回到实现前的前提判断

## 预期效果

优化后的 `ahe-increment` 应该具备这些特征：

- 不只是“分析变更影响”，而是能稳定收敛一轮安全的增量更新包
- 更容易决定到底该回 `ahe-spec-review`、`ahe-design-review`、`ahe-tasks-review` 还是重新进入实现
- 更少出现旧批准、旧 active task、旧验证证据被误用的情况
- 与 `ahe-workflow-router`、`ahe-hotfix`、`ahe-test-driven-dev` 的契约更一致
