# MDC 场景 02 模拟运行报告

## 场景信息

- 场景目录：`workflow-skills/mdc-eval-sample-pack/02-approved-spec-no-design/`
- 场景名称：规格已批准，但尚无设计

## 本次检查方式

1. 读取场景前置工件
2. 对照 `mdc-workflow-starter` 的路由顺序逐项判断
3. 对照 `mdc-design` 的进入条件和 handoff 规则判断是否连贯

## 前置工件判断

场景中已有 approved requirement spec，但不存在 approved design。

这意味着：

- 不应回退到规格起草
- 也不应跳过设计直接进入任务拆分或实现
- 当前最合理的下一步是进入设计阶段

## 对 `mdc-workflow-starter` 的路由推导

当前规则下：

1. 没有热修复证据，不命中 `mdc-hotfix`
2. 没有变更证据，不命中 `mdc-increment`
3. 已有 approved spec，不命中 `mdc-specify`
4. 缺少 approved design，因此命中 `mdc-design`

因此正确下游应为：

`mdc-design`

## 对 `mdc-design` 的进入适配性检查

`mdc-design` 的目标是：

- 读取 approved spec 作为设计输入
- 提出可比较的实现方案并给出推荐
- 形成设计说明
- handoff 到 `mdc-design-review`

这与场景 02 完全一致。

## 模拟结果

### 实际首个应命中 skill

`mdc-workflow-starter`

### 实际下游应命中 skill

`mdc-design`

### 预期 handoff

`mdc-design -> mdc-design-review`

## 结论

PASS

## 通过项

- 不会误路由回 `mdc-specify`
- 不会跳过设计直接进入 `mdc-tasks`
- `mdc-design` 的前置条件、目标和 handoff 与场景完全对齐

## 风险提示

如果后续团队允许更轻量的设计补丁流程，需要单独定义何时可直接进入 review，而不是在 starter 中混入模糊规则。
