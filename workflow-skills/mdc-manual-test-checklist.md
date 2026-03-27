# MDC Skills 手工试跑 Checklist

这份清单用于团队手工验证 MDC skills 是否能按预期触发、路由和串联。

适用对象：

- 需要验收这套 MDC skills 的设计者
- 首次接入这套流程的团队成员
- 需要做回归验证的维护者

## 试跑前准备

- [ ] 确认 `.cursor/skills/` 下的 MDC skills 已存在
- [ ] 确认已准备好要测试的场景目录
- [ ] 确认当前只测试一个场景，避免多个证据同时干扰
- [ ] 打开对应场景 README，核对前置工件是否齐全
- [ ] 准备好记录结果的表格或文档

## 推荐使用的测试资产

- 场景说明：`workflow-skills/mdc-skills-eval-prompts.md`
- 样例包：`workflow-skills/mdc-eval-sample-pack/`
- 入口 eval：`.cursor/skills/mdc-workflow-starter/evals/evals.json`

## 每个场景的执行步骤

### Step 1：进入场景目录

- [ ] 选择一个场景目录
- [ ] 核对该目录中的 spec / design / tasks / progress / change / hotfix 证据是否与 README 一致
- [ ] 确认没有多余的变更或热修复证据造成串扰

### Step 2：投喂用户 Prompt

- [ ] 从场景 README 中复制 prompt
- [ ] 原样输入，不要改写措辞
- [ ] 不补充额外上下文，除非该场景 README 明确要求

### Step 3：观察首个命中 skill

- [ ] 是否先命中 `mdc-workflow-starter`
- [ ] 是否先做 phase routing，而不是直接进入设计/任务/实现
- [ ] 是否引用了正确的证据来判断阶段

### Step 4：观察下游路由

- [ ] 是否路由到 README 里期望的目标 skill
- [ ] 是否没有跳过 review / gate
- [ ] 是否没有走到错误支线

### Step 5：观察 handoff 质量

- [ ] 是否明确说明“当前阶段”
- [ ] 是否明确说明“证据”
- [ ] 是否明确说明“下一 skill”
- [ ] 是否明确说明“阻塞项或缺失工件”

### Step 6：记录结果

- [ ] 填写该场景的 PASS / PARTIAL / FAIL
- [ ] 记录实际命中链路
- [ ] 记录是否有跳步
- [ ] 记录是否存在模糊 handoff

## 推荐记录模板

```markdown
## Eval: <场景名称>

- 场景目录:
- Prompt:
- 实际首个命中 skill:
- 实际下游 skill:
- 是否先做了 routing:
- 是否说明了 routing 证据:
- 是否跳过 review / gate:
- handoff 是否清晰:
- 结论: PASS | PARTIAL | FAIL
- 问题记录:
- 建议修正:
```

## 通过标准

### 入口级最低标准

- [ ] 5 个主场景里，至少 4 个先命中 `mdc-workflow-starter`
- [ ] 5 个主场景里，至少 4 个被正确路由到期望 skill
- [ ] 不出现“直接进入实现”的严重越权

### 主链级最低标准

- [ ] 从 `mdc-specify` 到 `mdc-implement` 的主链没有明显断链
- [ ] `mdc-implement` 之后能明确给出完整质量链顺序
- [ ] completion 相关结论不会在没有 fresh evidence 的情况下提前出现

### 支线级最低标准

- [ ] 有明确变更证据时优先进入 `mdc-increment`
- [ ] 有明确热修复证据时优先进入 `mdc-hotfix`
- [ ] 支线不会绕过 review / regression / completion discipline

## 常见失败信号

- [ ] 用户一说“继续”就直接开始写代码
- [ ] 已存在 draft spec，却被当作 approved spec
- [ ] 需求变更场景直接进入 `mdc-implement`
- [ ] 热修复场景跳过复现或回归
- [ ] 只做 review 的请求被错误地送回 `mdc-design` 或 `mdc-specify`
- [ ] handoff 只说“下一步继续”，但没说具体 skill

## 发现问题后的处理建议

### 如果是入口误触发

- 检查 skill description 是否太弱或太宽
- 检查 `mdc-workflow-starter` 是否缺少特定场景的路由规则

### 如果是主链断链

- 检查上游 skill 的 handoff 文案是否与下游 skill 名称一致
- 检查阶段前置条件是否写得太模糊

### 如果是支线绕过纪律

- 检查 `mdc-increment` / `mdc-hotfix` 是否明确要求回到 review / gate

## 建议执行顺序

建议按下面顺序跑：

1. `01-new-requirement`
2. `02-approved-spec-no-design`
3. `03-approved-plan-ready-implement`
4. `04-change-request`
5. `05-hotfix`

然后再补跑近似误触发场景：

6. 纯概念解释
7. review-only 请求
