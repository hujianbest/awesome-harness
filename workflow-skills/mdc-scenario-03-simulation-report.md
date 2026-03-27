# MDC 场景 03 模拟运行报告

## 场景信息

- 场景目录：`workflow-skills/mdc-eval-sample-pack/03-approved-plan-ready-implement/`
- 场景名称：任务计划已批准，可进入实现

## 本次检查方式

1. 读取场景前置工件
2. 对照 `mdc-workflow-starter` 的路由顺序逐项判断
3. 对照 `mdc-implement` 的执行规则、handoff 顺序和门禁链判断是否连贯

## 前置工件判断

场景中存在：

- approved requirement spec
- approved design doc
- approved task plan
- `task-progress.md`

其中进度记录明确给出：

- current phase: implement
- active task: `TASK-001`
- suggested next skill: `mdc-implement`

这意味着：

- 主链 requirements、design、tasks 三个上游阶段都已完成
- 当前存在唯一活动任务
- 当前最合理的下一阶段应是实现

## 对 `mdc-workflow-starter` 的路由推导

当前规则下：

1. 没有热修复证据，不命中 `mdc-hotfix`
2. 没有变更证据，不命中 `mdc-increment`
3. 不满足“缺少 approved spec”
4. 不满足“缺少 approved design”
5. 不满足“缺少 approved task plan”
6. 存在未完成的计划任务，因此命中 `mdc-implement`

因此正确下游应为：

`mdc-implement`

## 对 `mdc-implement` 的进入适配性检查

`mdc-implement` 的关键前置条件与场景一致：

- task plan 已通过 review
- 一次只做一个 active task
- 必须保持 TDD 倾向
- 完成后不能直接宣称 done，必须经过固定质量链

当前明确的后续顺序是：

```text
mdc-implement -> mdc-bug-patterns -> mdc-test-review -> mdc-code-review -> mdc-traceability-review -> mdc-regression-gate -> mdc-completion-gate
```

## 模拟结果

### 实际首个应命中 skill

`mdc-workflow-starter`

### 实际下游应命中 skill

`mdc-implement`

### 预期后续顺序

`mdc-implement -> mdc-bug-patterns -> mdc-test-review -> mdc-code-review -> mdc-traceability-review -> mdc-regression-gate -> mdc-completion-gate`

## 结论

PASS

## 通过项

- starter 能在 spec、design、task plan 都 approved 时继续向实现推进
- 当前进度证据足以支撑实现阶段判断
- `mdc-implement` 明确约束一次只处理一个 active task
- 实现后的质量链顺序明确且固定

## 风险提示

如果未来允许更灵活的实现中断恢复，需要补一份更细的进度记录模板，避免不同团队对“active task”理解不一致。
