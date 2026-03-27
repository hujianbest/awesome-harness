# MDC 场景 01 模拟运行报告

## 场景信息

- 场景目录：`workflow-skills/mdc-eval-sample-pack/01-new-requirement/`
- 场景名称：全新需求进入规格阶段

## 本次检查方式

本次采用规则级模拟检查：

1. 读取场景前置工件说明
2. 对照 `mdc-workflow-starter` 的当前路由规则逐项判断
3. 对照 `mdc-specify` 的进入条件与 handoff 预期判断是否连贯

## 前置工件判断

该场景故意不提供任何已批准的 spec、design、task plan。

这意味着：

- 没有主链上游批准工件
- 没有变更或热修复证据
- 当前应被判定为一个真正的 MDC 起点

## 对 `mdc-workflow-starter` 的路由推导

按照当前规则：

1. 没有热修复证据，不命中 `mdc-hotfix`
2. 没有变更证据，不命中 `mdc-increment`
3. 没有 approved requirement spec，因此命中 `mdc-specify`

因此正确下游应为：

`mdc-specify`

## 对 `mdc-specify` 的进入适配性检查

`mdc-specify` 的职责是：

- 先澄清需求、范围、角色与约束
- 不直接进入设计、任务或实现
- 产出规格草案
- handoff 到 `mdc-spec-review`

这与场景 01 完全匹配。

## 模拟结果

### 实际首个应命中 skill

`mdc-workflow-starter`

### 实际下游应命中 skill

`mdc-specify`

### 预期 handoff

`mdc-specify -> mdc-spec-review`

## 结论

PASS

## 通过项

- 主入口路由对这个场景清晰
- 不会误入 `mdc-increment` 或 `mdc-hotfix`
- 不会直接落到 `mdc-design`、`mdc-tasks` 或 `mdc-implement`
- `mdc-specify` 的职责边界与场景完全对齐

## 风险提示

后续如果 starter 增加更多弱信号判断，仍要防止把普通咨询误判成项目启动。

## 下一步建议

继续检查场景 02，验证在已有 approved spec、但没有 approved design 的情况下，是否稳定进入 `mdc-design`。
