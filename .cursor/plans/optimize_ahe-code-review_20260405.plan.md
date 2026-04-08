# 优化 `ahe-code-review` 方案

## 目标

把 `skills/ahe-code-review/SKILL.md` 从“能做基本代码评审”的 skill，提升为“能稳定消费上游实现与测试证据、判断实现级正确性与局部设计质量、并把结论安全交给 `ahe-traceability-review` 的高质量代码评审 skill”。

本次优化不改变 AHE 主链契约：

- 仍然由 `ahe-code-review` 负责实现级质量判断，而不是替代 `ahe-test-review` / `ahe-traceability-review` / `ahe-regression-gate`
- 仍然在 `ahe-test-review` 之后、`ahe-traceability-review` 之前使用（full / standard）
- 仍然通过 `通过 | 需修改 | 阻塞` 给出唯一下一步

## 当前问题

当前 `ahe-code-review` 已经覆盖正确性、设计一致性、可维护性和错误处理，但还存在几个高价值短板：

- 缺少明确消费 `ahe-test-review` 记录、`ahe-test-driven-dev` 实现交接块和 `ahe-bug-patterns` 风险上下文的要求
- 与 `ahe-traceability-review` 的边界偏模糊，容易把 code review 做成简化版追溯性评审
- 没有明确说明 full / standard 与 lightweight 的 profile 差异
- 输出还不够像可继续交接的 review artifact，缺少“上游已消费证据”和“本轮评审焦点”
- 对安全边界、并发 / 状态一致性、可观测性等高价值代码风险切片覆盖不足
- `Next Action` 仍偏自然语言，不够贴合 canonical `ahe-*` handoff
- 阻塞条件太粗，没把“缺少上游 review 记录”“diff / 触碰面不清楚”这类前提说透

## 优化方向

### 1. 增加角色定位与上下游边界

明确：

- 本 skill 负责实现级正确性、局部设计一致性、错误处理与可维护性判断
- 不替代 `ahe-test-review` 的测试质量裁决
- 不替代 `ahe-traceability-review` 的工件链路一致性检查
- 不替代 `ahe-regression-gate` 的回归执行

为什么这么改：

- 高质量 code review 的前提是边界稳定，否则很容易和 traceability / regression gate 混线

主要参考：

- `skills/ahe-test-review/SKILL.md`
- `skills/ahe-traceability-review/SKILL.md`
- `skills/ahe-regression-gate/SKILL.md`

### 2. 增加 pre-flight 输入与上游证据消费要求

要求至少读取：

- `AGENTS.md` 中与当前项目相关的 coding / review 规范（如果存在）
- `ahe-test-driven-dev` 的实现交接块
- `ahe-test-review` 记录
- `ahe-bug-patterns` 记录（如当前链路要求）
- 当前 diff / 触碰工件 / 关键实现范围

为什么这么改：

- code review 不应脱离实现证据和测试 verdict 单独飘着做判断

主要参考：

- `skills/ahe-test-driven-dev/SKILL.md`
- `skills/ahe-test-review/SKILL.md`
- `references/superpowers-main/skills/requesting-code-review/SKILL.md`

### 3. 收紧“实现级”评审边界，避免与 traceability 混线

明确区分：

- `ahe-code-review` 检查局部 API / 模块 / 状态 / 错误处理 / 代码结构是否合理
- `ahe-traceability-review` 负责规格、设计、任务、实现、验证记录之间的全链路一致性

为什么这么改：

- 这样可以避免 code review 重复做 artifact matrix，同时保留对“偷偷扩 scope”或“局部设计漂移”的实现级警报

主要参考：

- `skills/ahe-traceability-review/SKILL.md`
- `references\\gstack-main\\review\\SKILL.md`

### 4. 增加高价值代码风险切片

补强如下维度：

- trust boundary / 安全敏感路径
- 状态切换、一致性、并发 / 重入风险
- 错误处理与降级路径
- 可读性 / 复杂度 / 隐性耦合
- 可观测性与调试性（在项目约定适用时）

为什么这么改：

- 高质量 code review 不能只停留在“代码好不好读”，还要显式检查最容易在生产出问题的实现风险

主要参考：

- `references/everything-claude-code-main/skills/security-review/SKILL.md`
- `references/everything-claude-code-main/skills/coding-standards/SKILL.md`
- `references/gstack-main/review/SKILL.md`

### 5. 升级输出为可继续交接的 review artifact

要求至少显式说明：

- 上游已消费证据
- 本轮评审焦点 / 触碰面
- 发现项与代码风险
- 哪些内容明确不在本轮 code review 范围内
- 给 `ahe-traceability-review` 的简短提示

为什么这么改：

- 这样 code review 的结果才不只是 verdict，而是后续链路可消费的输入

主要参考：

- `skills/ahe-test-review/SKILL.md`
- `references/gstack-main/review/SKILL.md`

### 6. 收紧 canonical handoff

要求 `Next Action Or Recommended Skill` 优先写：

- `ahe-traceability-review`
- `ahe-test-driven-dev`

为什么这么改：

- router 和其它 AHE 节点都已经在收紧 canonical `ahe-*` handoff

主要参考：

- `skills/ahe-workflow-router/SKILL.md`

### 7. 补充 profile 说明

明确：

- full / standard 主链默认包含 code-review
- lightweight 默认不经过本节点；若手动调用，应视为补充性评审

为什么这么改：

- 这能减少“lightweight 为什么没有 code-review 记录”的误解，并避免非法 next-step

主要参考：

- `skills/ahe-workflow-router/SKILL.md`

### 8. 强化阻塞条件与失败模式

明确在以下场景应返回 `阻塞`：

- full / standard 正式链路中缺少 `ahe-test-review` 记录
- 关键 diff / 触碰工件 / 上游 handoff 不可读
- 无法把实现范围和当前任务对齐

为什么这么改：

- 这样能减少“上下文不全却硬给 verdict”的伪通过

主要参考：

- `skills/ahe-test-review/SKILL.md`
- `references/gstack-main/review/SKILL.md`

## 明确不做的事

- 不把 `ahe-code-review` 写成第二个 traceability review
- 不把它写成第二个 regression gate
- 不把它扩成独立 security review
- 不改动其它质量节点职责

## 计划中的实际改动

会对 `skills/ahe-code-review/SKILL.md` 做一轮聚焦增强，预计包括：

- 增加角色边界和 pre-flight 输入
- 明确实现级边界与 traceability / regression 的分工
- 增加高价值代码风险切片
- 输出升级为可继续交接的 review artifact
- 收紧 canonical handoff
- 增加 profile 说明与阻塞条件

## 预期效果

优化后的 `ahe-code-review` 应该具备这些特征：

- 更像正式实现质量 gate，而不是泛泛 checklist
- 更容易与 `ahe-test-review`、`ahe-traceability-review`、`ahe-regression-gate` 串成一致链路
- 更少出现“测试是绿的，但实现本身仍有结构性风险”的漏判
