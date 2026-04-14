---
name: ahe-test-review
description: 评审当前任务的测试资产。判断 fail-first 有效性、行为覆盖、风险覆盖是否足以支持进入 ahe-code-review。防止浅层"绿测"冒充可信验证。
---

# AHE Test Review

评审测试资产，判断 fail-first、行为覆盖和风险覆盖是否足以支持 `ahe-code-review`。运行在 `ahe-bug-patterns` 之后。

## When to Use

适用：bug-patterns 完成后判断测试质量、code review 前的测试评审、用户要求 test review。

不适用：写/修测试 → `ahe-test-driven-dev`；评审代码 → `ahe-code-review`；阶段不清 → `ahe-workflow-router`。

## Hard Gates

- test review 通过前不得进入 code review
- 输入工件不足不得开始评审
- reviewer 不修测试、不继续实现

## Workflow

### 1. 建立证据基线

读实现交接块、新增/修改测试、bug-patterns 记录、AGENTS.md 测试约定、规格/设计片段、task-progress.md。

### 2. 多维评分与挑战式审查

5 个维度 0-10 评分：fail-first 有效性、行为覆盖、风险覆盖、测试设计质量、下游就绪度。任一关键维度 < 6 不得通过。

### 3. 正式 checklist 审查

3.1 **Fail-first & RED/GREEN**：RED 是否对应当前行为缺口？GREEN 是否来自本次实现？
3.2 **行为价值与验收映射**：测试是否覆盖任务关键行为？是否映射回验收标准？
3.3 **风险覆盖与边界**：是否覆盖 bug-patterns 识别的风险？边界/null/错误路径？
3.4 **测试设计质量**：mock 是否限定在真正边界？测试是否独立可重复？
3.5 **下游就绪度**：测试质量是否足以让 code-review 做可信判断？

### 4. 形成 verdict

- `通过`：所有维度 >= 6，测试足以支持 code review
- `需修改`：findings 可 1-2 轮定向修订
- `阻塞`：测试过于薄弱/核心行为未覆盖/findings 无法定向回修

Findings 带 severity（critical/important/minor）和分类（USER-INPUT/LLM-FIXABLE）。

### 5. 写 review 记录

保存到 `docs/reviews/test-review-<task>.md`。回传结构化摘要给父会话。返回遵循 `ahe-workflow-router/references/reviewer-return-contract.md`。

## Red Flags

- 不读 handoff 就审测试
- "测试文件存在"等同于"测试充分"
- 忽略无效 RED/GREEN
- 忽略 bug-patterns 识别的风险
- 评审中修测试
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings、gaps 和唯一下一步
- [ ] 结构化摘要含 next_action_or_recommended_skill
- [ ] 结论足以让父会话路由
