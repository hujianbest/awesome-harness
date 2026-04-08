# 优化 `ahe-test-driven-dev` 方案

## 目标

把 `skills/ahe-test-driven-dev/SKILL.md` 从“能做 TDD 且默认偏 C++/GoogleTest 的实现 skill”，提升为“能稳定承担 AHE 唯一实现入口、产出高质量实现证据与高质量后续交接工件的 skill”。

本次优化不改变 AHE 主链契约：

- 仍然只有 `ahe-test-driven-dev` 作为实现阶段统一入口
- 仍然坚持一次只推进一个活跃任务
- 仍然要求在进入 Red-Green-Refactor 前先做真人测试设计确认
- 仍然由 `ahe-workflow-router` 管理实现后的恢复编排
- 仍然不把 `ahe-test-driven-dev` 变成 `ahe-test-review`、`ahe-regression-gate` 或 `ahe-bug-patterns`

## 当前问题

当前 `ahe-test-driven-dev` 已经有正确的大方向，但仍存在几个影响交付质量的短板：

- 前半段是 AHE 实现入口契约，后半段是较长的 C++/GoogleTest 教程，执行重心不够稳定
- 虽然要求写回 fresh evidence 和推荐下一步，但没有定义稳定的实现交接块，导致下游 review / gate 难以机械读取
- fail-first 被强调了，但“什么算有效 RED / 什么不算”仍不够清晰
- 非 C++ 场景只写了“当前未覆盖”，没有给出可执行的最小通用实现契约
- 有真人测试设计确认门禁，但缺少对测试设计本身质量的轻量自检
- 与 `ahe-test-review`、`ahe-regression-gate`、`ahe-bug-patterns` 的边界不够锐利，容易出现重复验证或范围漂移
- gate 回流或 hotfix 回流进入实现时，缺少更明确的“如何带着发现项重新进入当前任务”的协议
- 细节上还存在 `AGENTS.md` / `Agents.md`、`HDT` 等表达不一致，影响可信度

## 优化方向

### 1. 重排文档结构，优先突出“实现入口契约”

把 skill 的前半部分聚焦为：

- 什么时候能进入实现
- 如何锁定唯一活跃任务
- 如何完成测试设计确认
- 如何执行 RED / GREEN / REFACTOR
- 如何写回实现证据与下一步 handoff

把 C++ / GoogleTest 细节保留为后置附录式指南，而不是让它压过 AHE 实现主契约。

为什么这么改：

- 当前 skill 最大价值不只是“TDD 教程”，而是 AHE 主链里唯一实现入口
- 先稳定执行和交接契约，才能让下游 review / gate 稳定工作

主要参考：

- `references/everything-claude-code-main/skills/tdd-workflow/SKILL.md`
- `references/superpowers-main/skills/test-driven-development/SKILL.md`
- `skills/ahe-test-driven-dev/SKILL.md`

### 2. 增加稳定的“实现交接块”

要求在实现完成或回流修订完成后，至少写回：

- 当前任务 ID 与目标
- 触碰工件
- RED 证据：命令、失败摘要、失败为何符合预期
- GREEN 证据：命令、通过摘要、关键结果
- 与任务计划中的测试设计种子相比，有无调整
- 剩余风险 / 已知限制
- 待进入的 canonical `Next Action Or Recommended Skill`

为什么这么改：

- 这能把“实现完成”从口头描述升级为可被 `ahe-test-review` / `ahe-workflow-router` / 后续 gate 消费的稳定产物
- 也能减少 review 阶段反复追问“你到底改了什么、怎么证明”

主要参考：

- `references/everything-claude-code-main/skills/verification-loop/SKILL.md`
- `references/superpowers-main/skills/verification-before-completion/SKILL.md`
- `skills/ahe-workflow-router/SKILL.md`

### 3. 明确有效 RED / GREEN 的判定标准

补强规则，明确：

- 没有真正执行的失败测试，不算 RED
- 与当前行为无关的环境故障、无关编译错误，不算有效 RED
- 只有看到与预期行为对应的失败，才算完成 fail-first
- GREEN 后至少要有当前任务对应的新鲜通过证据，而不是复用旧结果

为什么这么改：

- 高质量实现入口不能只说“先写失败测试”，还要定义什么样的失败是可信的
- 这也能让 `ahe-test-review` 的 fail-first 检查更容易对齐

主要参考：

- `references/everything-claude-code-main/skills/tdd-workflow/SKILL.md`
- `references/superpowers-main/skills/test-driven-development/SKILL.md`

### 4. 补一层轻量“测试设计自检”

在真人确认前，要求快速检查：

- 是否覆盖核心行为
- 是否存在关键反向 / 边界场景
- 当前测试能抓住哪类错误实现
- 是否把 mock 限定在真正的外部边界，而不是 mock 自己的逻辑

为什么这么改：

- 真人确认是必要门禁，但 skill 本身也应该帮助产出更强的测试设计
- 这样能减少“测试设计确认过了，但测试其实很弱”的问题

主要参考：

- `references/longtaskforagent-main/skills/long-task-tdd/SKILL.md`
- `skills/ahe-test-driven-dev/testing-anti-patterns.md`

### 5. 为非 C++ 场景补一个“最小通用执行契约”

若当前项目不是 C++ / GoogleTest：

- 仍然必须执行相同的测试设计确认、RGR、fresh evidence、交接块流程
- 明确记录当前语言 / 框架 / 命令入口
- 说明当前附录只提供 C++ 深度示例，但实现契约本身仍然适用

为什么这么改：

- 当前 skill 已经是 AHE 唯一实现入口，不能在非 C++ 场景下只停留在“未覆盖”
- 即使没有完整语言专用 cookbook，也应保证主链行为不失真

主要参考：

- `references/everything-claude-code-main/skills/python-testing/SKILL.md`
- `references/everything-claude-code-main/skills/golang-testing/SKILL.md`
- `references/everything-claude-code-main/skills/rust-testing/SKILL.md`

### 6. 收紧与下游质量节点的边界

明确说明：

- `ahe-test-review` 关注 fail-first 纪律、测试质量和当前任务级证据
- `ahe-bug-patterns` 关注缺陷模式排查，不替代当前 skill 的实现与测试纪律
- `ahe-regression-gate` 负责更广义的回归验证与 gate 记录，不由当前 skill 代做

为什么这么改：

- 当前 skill 如果不讲清边界，最容易出现“自己先把 review / gate 做了一半”
- 清晰边界能减少实现阶段 scope creep

主要参考：

- `skills/ahe-test-review/SKILL.md`
- `skills/ahe-bug-patterns/SKILL.md`
- `skills/ahe-regression-gate/SKILL.md`

### 7. 增加回流修订协议

当当前 skill 是因为 hotfix、review 或 gate 回流而重新进入时，要求：

- 明确本次回流来源
- 锚定发现项、失败用例或阻塞证据
- 只修当前任务和当前回流范围，不顺手扩张
- 修订完成后把新的 fresh evidence 和 canonical 下一步写回

为什么这么改：

- 这能让 `ahe-hotfix` 与各类 review / gate 回流进入实现时更稳定
- 也能减少“回流一次就把质量链重跑成起点”的混乱

主要参考：

- `skills/ahe-hotfix/SKILL.md`
- `references/gstack-main/investigate/SKILL.md`
- `references/everything-claude-code-main/skills/continuous-agent-loop/SKILL.md`

## 明确不做的事

- 不把当前 skill 扩写成所有语言的完整测试手册
- 不把 `ahe-test-driven-dev` 变成下游 review / gate 的替代品
- 不新增第二条实现入口
- 不改变 `ahe-workflow-router` 已拥有的恢复编排权

## 计划中的实际改动

会对 `skills/ahe-test-driven-dev/SKILL.md` 做一轮聚焦增强，预计包括：

- 重排结构，先写实现入口契约，再放 C++ / GoogleTest 细节
- 增加高质量实现交接块
- 收紧有效 RED / GREEN 与新鲜证据规则
- 增加测试设计自检与回流修订协议
- 增加非 C++ 场景的最小通用执行契约
- 明确与 `ahe-test-review`、`ahe-bug-patterns`、`ahe-regression-gate` 的边界
- 修正命名和表达不一致问题

## 预期效果

优化后的 `ahe-test-driven-dev` 应该具备这些特征：

- 不只是“会要求写测试”，而是能稳定驱动高质量单任务实现
- 产出的实现证据更容易被后续 review / gate 直接消费
- 在 hotfix / gate 回流 / 非 C++ 场景下也能保持主链契约稳定
- 更少出现“实现做完了，但 handoff 不够硬、下游还要补脑”的情况
