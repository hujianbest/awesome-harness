# Product Insights To Coding Bridge Walkthrough

- 状态: current reference-slice evidence
- 日期: 2026-04-11
- 目的: 用当前 `T080 / T090 / T100` 实现面验证第一条 `product-insights -> coding` bridge seam 已经具备最小闭环。

## 1. 最小 bridge payload

当前 bridge 仍然通过现有 contracts 组合表达，而不是新增特权 contract。

- `bridge artifact`: `spec-bridge`
- `bridge evidence`: `bridge-evidence`
- source node: `product-insights.bridge-ready`
- target node: `coding.bridge-intake`

当前最小 payload 需要覆盖：

- 要解决的问题
- 目标对象或使用语境
- 预期结果
- 当前选中的机会 / wedge
- scope 边界与明确不做什么
- 关键未知项
- 关键判断依据、主要来源、已做 probe 与未关闭假设

## 2. Acceptance Matrix

| verdict | records / outputs | session transition | evidence trace |
| --- | --- | --- | --- |
| `accepted` | `HandoffRecord` + `bridge-lineage` | `handoff-pending -> active` | 接受 verdict 写入 `bridge-lineage` |
| `accepted-with-gaps` | `HandoffRecord` + `bridge-lineage` | `handoff-pending -> active` | gap 仍进入 evidence，而不是隐式带过 |
| `needs-clarification` | `HandoffRecord` + `bridge-lineage` + `ReworkRequest` | `handoff-pending -> review-hold` | 缺口与补足方向显式回流 |
| `rejected-return-upstream` | `HandoffRecord` + `bridge-lineage` + `ReworkRequest` | `handoff-pending -> rework` | 拒绝原因和回流输入留痕 |

## 3. 成功路径 Walkthrough

1. `Product Insights Pack` 在 `bridge-ready` 节点交出 `spec-bridge` 与 `bridge-evidence`。
2. `Coding Pack` 在 `bridge-intake` 以 `accepted-with-gaps` 接住输入，并把 verdict 写入 `bridge-lineage` evidence。
3. 下游继续走 `specify -> design -> tasking -> implement -> review -> verify -> closeout` 主链。
4. `closeout-summary` 和 `closeout-record` 保留了从 `spec-bridge` 到下游 closeout 的可追溯链路。

这一条路径证明：

- bridge 不依赖隐式聊天上下文
- acceptance 是显式 verdict
- closeout 能回指上游 bridge，而不是在 coding 侧切断 lineage

## 4. 回流路径 Walkthrough

1. 上游仍然交出 `spec-bridge` 与 `bridge-evidence`。
2. 下游 intake 判断 scope ownership 和风险归属仍不清楚。
3. `Coding Pack` 写入 `needs-clarification` verdict，并生成 `ReworkRequest`。
4. session 进入 `review-hold`，上游必须基于缺口重新产出新的 bridge surface。

这一条路径证明：

- 回流是受控动作，不是异常补丁
- 目标 pack 没有在未接受前“顺手补锅”
- 缺口信息以正式输入形式返回，而不是口头说明

## 5. 当前 defer list

- 还没有复杂多 pack orchestration engine；当前只验证第一条 reference bridge。
- `ReworkRequest` 目前是 runtime helper，而不是单独 materialize 的 artifact surface。
- acceptance 目前是 fixture-driven runtime helper，还没有接进完整的 policy-evaluated runtime loop。
- walkthrough 目前以 reference evidence 和 tests 证明闭环，还没有自动生成完整 workspace demo surface。
