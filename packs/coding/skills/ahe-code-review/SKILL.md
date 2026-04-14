---
name: ahe-code-review
description: 评审实现代码的正确性、本地设计一致性、状态安全和可维护性。防止"测试通过"掩盖实现问题。运行在 ahe-test-review 之后。
---

# AHE Code Review

评审实现代码质量。判断正确性、设计一致性、状态/错误/安全、可读性和下游追溯就绪度。运行在 `ahe-test-review` 之后，决定是否可进入 `ahe-traceability-review`。

## When to Use

适用：test review 通过后评审代码、用户要求 code review。

不适用：评审测试 → `ahe-test-review`；写/修代码 → `ahe-test-driven-dev`；阶段不清 → `ahe-workflow-router`。

## Hard Gates

- code review 通过前不得进入 traceability review
- 输入工件不足不得开始
- reviewer 不改代码、不继续实现

## Workflow

### 1. 建立证据基线

读实现交接块、代码变更、test-review 记录、AGENTS.md coding 约定、规格/设计片段、task-progress.md。

### 2. 多维评分与挑战式审查

5 维度 0-10 评分：正确性、设计一致性、状态/错误/安全、可读性、下游追溯就绪度。任一关键维度 < 6 不得通过。

### 3. 正式 checklist 审查

3.1 **正确性**：实现是否真正完成了任务目标？逻辑是否有 off-by-one、边界遗漏？
3.2 **设计一致性**：实现是否遵循已批准设计？偏离是否有理由且可追溯？
3.3 **状态/错误/安全**：错误处理是否完备？状态转换是否安全？是否有安全隐患？
3.4 **可读性**：命名是否清晰？结构是否合理？是否有过早优化或死代码？
3.5 **下游就绪度**：代码是否足以让 traceability-review 做可信判断？实现交接块是否完整？

### 4. 形成 verdict

- `通过`：所有维度 >= 6，代码足以支持追溯评审
- `需修改`：findings 可 1-2 轮定向修订
- `阻塞`：核心逻辑错误/安全漏洞/findings 无法定向回修

Findings 带 severity 和 USER-INPUT/LLM-FIXABLE 分类。给出代码风险和追溯评审提示。

### 5. 写 review 记录

保存到 `docs/reviews/code-review-<task>.md`。回传结构化摘要。返回遵循 reviewer-return-contract。

## Red Flags

- 不读实现交接块就审代码
- "测试通过"等同于"代码正确"
- 忽略错误处理/安全风险
- 评审中改代码
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings、code risks 和唯一下一步
- [ ] 结构化摘要含 next_action_or_recommended_skill
