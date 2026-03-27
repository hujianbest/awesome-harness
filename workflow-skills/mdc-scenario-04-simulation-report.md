# MDC 场景 04 模拟运行报告

## 场景信息

- 场景目录：`workflow-skills/mdc-eval-sample-pack/04-change-request/`
- 场景名称：需求变更进入 increment 支线

## 本次检查方式

1. 读取场景前置工件
2. 对照 `mdc-workflow-starter` 的路由顺序逐项判断
3. 对照 `mdc-increment` 的进入条件、影响分析和回流规则判断是否连贯

## 前置工件判断

场景中已有 approved spec、design、task plan，同时提供了明确的变更说明：

- 审批通过后，需要自动抄送项目经理
- 该变更属于需求范围追加
- requirement spec、design doc、task plan 都可能受影响

这意味着：

- 当前不是普通实现推进
- 也不是热修复
- 应优先进入变更影响同步分支

## 对 `mdc-workflow-starter` 的路由推导

当前规则下：

1. 没有热修复证据，不命中 `mdc-hotfix`
2. 存在明确变更证据，因此命中 `mdc-increment`

因此正确下游应为：

`mdc-increment`

## 对 `mdc-increment` 的进入适配性检查

`mdc-increment` 的职责与场景一致：

- 先读取变更说明与现有主链工件
- 做 impact analysis
- 判断 spec、design、tasks 哪些需要同步
- 将下一步回流到合适的 review 或实现阶段

## 模拟结果

### 实际首个应命中 skill

`mdc-workflow-starter`

### 实际下游应命中 skill

`mdc-increment`

### 预期后续动作

- 分析影响面
- 记录同步项
- 视影响程度回流到 `mdc-spec-review`、`mdc-design-review`、`mdc-tasks-review` 或 `mdc-implement`

## 结论

PASS

## 通过项

- 变更证据会在主链推进判断之前被识别
- 不会误把该场景直接送进 `mdc-implement`
- `mdc-increment` 已明确要求 impact analysis 和工件同步

## 风险提示

如果后续需要区分“小变更只回 tasks-review”和“重大变更必须回 spec-review”，建议单独增加严重度分级示例。
