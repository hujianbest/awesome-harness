# 优化 `ahe-traceability-review` 方案

## 目标

把 `skills/ahe-traceability-review/SKILL.md` 从“能做基本追溯检查”的 skill，提升为“能稳定消费上游评审与实现证据、判断需求/设计/任务/实现/验证链路是否仍然闭合，并把结论安全交给 `ahe-regression-gate` 或正确回流节点的高质量追溯性评审 skill”。

本次优化不改变 AHE 主链契约：

- 仍然由 `ahe-traceability-review` 负责工件链路一致性判断，而不是替代 `ahe-code-review` / `ahe-regression-gate`
- 仍然在 `ahe-code-review` 之后、`ahe-regression-gate` 之前使用（full / standard）
- 仍然通过 `通过 | 需修改 | 阻塞` 给出唯一下一步

## 当前问题

当前 `ahe-traceability-review` 已经覆盖规格、设计、任务、实现、测试与验证的一致性，但还存在几个高价值短板：

- 缺少明确消费 `ahe-test-driven-dev` 实现交接块、`ahe-test-review`、`ahe-code-review` 等上游证据的要求
- 与 `ahe-code-review` 的边界偏模糊，容易把 traceability review 做成第二次代码评审
- 没有明确说明 full / standard 与 lightweight 的 profile 差异
- 输出还不够像可继续交接的 review artifact，缺少“上游已消费证据”“链路矩阵”“明确不在范围内”等结构
- 对 `阻塞` 的类型没有细分，容易把上游批准 / 编排问题错误地回流到实现修订
- 记录要求与 `ahe-finalize` 的证据矩阵、状态字段衔接还不够强

## 优化方向

### 1. 增加角色定位与上下游边界

明确：

- 本 skill 负责需求、设计、任务、实现、测试、验证之间的链路一致性判断
- 不替代 `ahe-code-review` 的实现质量判断
- 不替代 `ahe-regression-gate` 的新鲜验证执行
- 重点检查“被声称完成的内容”能否回指到已批准工件和验证证据

为什么这么改：

- traceability review 的价值在于工件链条，而不是重复看代码细节

主要参考：

- `skills/ahe-code-review/SKILL.md`
- `skills/ahe-regression-gate/SKILL.md`
- `skills/ahe-finalize/SKILL.md`

### 2. 增加 pre-flight 输入与上游证据消费要求

要求至少读取：

- `ahe-test-driven-dev` 的实现交接块
- `ahe-test-review` 记录
- `ahe-code-review` 记录
- 当前任务对应的规格 / 设计 / 任务锚点
- `task-progress.md` 当前状态

为什么这么改：

- 高质量追溯判断不能只看代码和一句“已完成”，必须消费整条上游证据链

主要参考：

- `skills/ahe-test-driven-dev/SKILL.md`
- `skills/ahe-test-review/SKILL.md`
- `skills/ahe-code-review/SKILL.md`

### 3. 引入链路矩阵式检查结构

把检查组织成明确链段：

- 规格 -> 设计
- 设计 -> 任务
- 任务 -> 实现
- 实现 -> 测试 / 验证
- 用户可见变化 / 文档 -> 当前交付声明（如适用）

为什么这么改：

- 这样更容易定位断链点，也更容易被 `ahe-finalize` 直接消费

主要参考：

- `skills/ahe-traceability-review/references/traceability-review-record-template.md`
- `references/longtaskforagent-main/skills/long-task-ats/SKILL.md`
- `references/everything-claude-code-main/skills/click-path-audit/SKILL.md`

### 4. 补充 profile 行为与 lightweight 规则

明确：

- full / standard 主链默认包含 traceability review
- lightweight 默认不经过本节点；若手动调用，应视为补充性评审

为什么这么改：

- 这能减少“为什么 finalize 里这条证据是 N/A”的误解，并避免非法 next-step

主要参考：

- `skills/ahe-workflow-router/SKILL.md`
- `skills/ahe-finalize/SKILL.md`

### 5. 升级输出为可继续交接的 review artifact

要求至少显式说明：

- 上游已消费证据
- 链路矩阵或关键链段结论
- 追溯缺口
- 漂移风险
- 明确不在本轮范围内
- 给 `ahe-regression-gate` 或回流节点的 canonical 下一步

为什么这么改：

- 这样 traceability 的结果才不只是 verdict，而是后续 gate 可继续消费的输入

主要参考：

- `skills/ahe-code-review/SKILL.md`
- `skills/ahe-finalize/SKILL.md`
- `references/everything-claude-code-main/skills/verification-loop/SKILL.md`

### 6. 收紧 canonical handoff 与 blocker 分类

要求 `Next Action Or Recommended Skill` 优先写：

- `ahe-regression-gate`
- `ahe-test-driven-dev`

同时补充：

- 若 `阻塞` 是实现修订类，回到 `ahe-test-driven-dev`
- 若 `阻塞` 是上游批准 / 工件缺失 / 编排错位，应在记录中明确要求经 `ahe-workflow-router` 重编排

为什么这么改：

- 这能减少“planning 问题被错误丢给实现阶段”的错路由

主要参考：

- `skills/ahe-code-review/SKILL.md`
- `skills/ahe-workflow-router/SKILL.md`

### 7. 强化记录要求与 finalize 对接

让 traceability review 的输出直接支持：

- `ahe-finalize` 的证据矩阵
- `task-progress.md` 的 review 状态更新
- 必要时对 README / RELEASE_NOTES / 其它受影响文档的同步提示

为什么这么改：

- traceability review 常常是发现“代码没错，但工件没跟上”的最后一道 review

主要参考：

- `skills/ahe-finalize/SKILL.md`
- `references/gstack-main/document-release/SKILL.md`

## 明确不做的事

- 不把 `ahe-traceability-review` 写成第二个 code review
- 不把它写成第二个 regression gate
- 不要求为每次小改动生成厚重 RTM 文档
- 不改动其它质量节点职责

## 计划中的实际改动

会对 `skills/ahe-traceability-review/SKILL.md` 做一轮聚焦增强，预计包括：

- 增加角色边界和 pre-flight 输入
- 引入链路矩阵式检查结构
- 增加 profile 说明
- 输出升级为可继续交接的 review artifact
- 收紧 canonical handoff 与 blocker 分类
- 强化与 finalize 的记录衔接

## 预期效果

优化后的 `ahe-traceability-review` 应该具备这些特征：

- 更像正式 evidence-chain gate，而不是泛泛一致性检查
- 更容易与 `ahe-code-review`、`ahe-regression-gate`、`ahe-finalize` 串成一致链路
- 更少出现“代码和测试都看起来对，但工件链已经断了”的漏判
