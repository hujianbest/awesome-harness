# T222: Garage WebEntry Governance And Review Surfaces

- Task ID: `T222`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为 `WebEntry` 增加 review、approval 与 governance surfaces，使浏览器入口在不越权的前提下消费共享治理语义，而不是在 UI 里私自定义审批逻辑。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T160-garage-local-first-web-control-plane.md`
  - `docs/features/F050-governance-model.md`
  - `docs/tasks/T040-garage-session-lifecycle-and-governance.md`
  - `docs/architecture/A120-garage-core-subsystems-architecture.md`

## 1. 任务目标

这一篇解决的是：

- 浏览器里如何做 review、approval 与 governance 提示
- WebEntry 如何消费共享治理语义
- UI 如何展示治理要求而不私自改写 gate 逻辑

## 2. 输入设计文档

- governance model
- session lifecycle 与 approval / review 主链
- WebEntry 的 local-first control plane

## 3. 本文范围

- review / approval / gate 的最小 UI surface
- governance 状态、阻断原因与证据缺口的展示方式
- UI 触发治理动作时的最小请求路径
- 与 session、evidence、trace 的最小关联方式

## 4. 非目标

- 不让 WebEntry 自己决定治理 verdict
- 不在这里重写 policy authoring 系统
- 不把 UI 做成重型管理后台

## 5. 交付物

- 一套 WebEntry governance surfaces 最小骨架
- 一组 review / approval / gate 的共享 readback 与 request 路径
- 一套阻断、待批与缺证据的展示规则

## 6. 实施任务拆解

### 6.1 冻结治理展示对象

- 明确 WebEntry 要展示哪些 gate、approval、review 与缺证据状态。
- 明确这些对象与共享治理语义的映射。

### 6.2 接通共享请求路径

- review、approval、closeout 等动作通过共享 session / governance seam 提交。
- 保证 UI 不能绕过共享治理主线。

### 6.3 收紧展示与解释边界

- 明确阻断原因、待确认项与补证据要求如何展示。
- 保持 UI 解释来自共享治理结果，而不是 UI 私有判断。

### 6.4 做最小验证闭环

- 验证 WebEntry 能稳定展示治理状态。
- 验证治理动作仍由共享 runtime 主线决定。

## 7. 依赖与并行建议

- 依赖 `16`、`27`
- 可与 `28` 并行，但共享治理 readback 语义应保持一致

## 8. 验收与验证

- WebEntry 已有 governance / review / approval surfaces 切片
- 浏览器 UI 不会私自改写治理语义
- 阻断、待批与缺证据状态可被稳定展示

## 9. 完成后进入哪一篇

- 进入更细的 WebEntry governance UX slices，若后续确有需要
