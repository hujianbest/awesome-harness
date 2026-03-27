# MDC 场景 05 模拟运行报告

## 场景信息

- 场景目录：`workflow-skills/mdc-eval-sample-pack/05-hotfix/`
- 场景名称：紧急缺陷进入 hotfix 支线

## 本次检查方式

1. 读取场景前置工件
2. 对照 `mdc-workflow-starter` 的路由顺序逐项判断
3. 对照 `mdc-hotfix` 的进入条件、复现要求和后续质量链判断是否连贯

## 前置工件判断

场景中已有主链工件，同时提供了明确缺陷证据：

- 审批通过后没有发送通知
- 这是需要优先修复的线上问题
- 已提供期望行为、实际行为、影响和复现步骤

这意味着：

- 当前不是普通实现推进
- 也不是普通需求增量
- 应优先进入热修复分支

## 对 `mdc-workflow-starter` 的路由推导

当前规则下：

1. 存在明确热修复证据，因此优先命中 `mdc-hotfix`
2. 不应继续主链，也不应误入 `mdc-increment`

因此正确下游应为：

`mdc-hotfix`

## 对 `mdc-hotfix` 的进入适配性检查

`mdc-hotfix` 的前置条件与场景完全匹配：

- 已知线上缺陷
- 有明确复现线索
- 需要最小修复
- 修复后仍需经过质量链验证

当前预期顺序是：

```text
mdc-hotfix -> mdc-bug-patterns -> mdc-test-review -> mdc-code-review -> mdc-traceability-review -> mdc-regression-gate -> mdc-completion-gate
```

## 模拟结果

### 实际首个应命中 skill

`mdc-workflow-starter`

### 实际下游应命中 skill

`mdc-hotfix`

### 预期后续顺序

`mdc-hotfix -> mdc-bug-patterns -> mdc-test-review -> mdc-code-review -> mdc-traceability-review -> mdc-regression-gate -> mdc-completion-gate`

## 结论

PASS

## 通过项

- starter 会优先识别热修复证据
- `mdc-hotfix` 强制要求先复现再修复
- 热修复完成后仍保留完整质量链，而不是因为紧急就跳过验证

## 风险提示

真实多轮对话里仍需继续观察：模型是否会稳定表达完整质量链，而不是只挑其中一个 review 或 gate 就停止。
