# T160: Garage Local-first Web Control Plane

- Task ID: `T160`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 `WebEntry` 落成 local-first control plane + UI，使浏览器入口通过共享 `SessionApi` 消费同一个 runtime，而不是复制出第二套 web-only runtime。
- 当前阶段: 完整架构主线下的第二组独立入口 implementation tracks
- 关联设计文档:
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`
  - `docs/architecture/A120-garage-core-subsystems-architecture.md`
  - `docs/features/F060-artifact-and-evidence-surface.md`

## 1. 任务目标

这一篇要把三类入口里的：

- `WebEntry`

从“文档上允许存在”推进到“实现上可规划落地”。

它要证明的是：

- `WebEntry` 默认是 local-first control plane，而不是先长成 remote SaaS
- 浏览器 UI 通过共享 runtime seam 工作，而不是复制一套新的 session / execution 流程
- web 入口和 CLI / host bridge 一样，也只能通过 `Bootstrap -> SessionApi -> Session` 进入系统

## 2. 输入设计文档

这一篇主要承接：

- `WebEntry` 作为一等入口 family
- `runtime home / workspace` 的分层与 dogfooding mode
- `SessionApi` 作为共享入口请求面
- execution layer 的共享 invocation seam
- workspace-first artifact / evidence surfaces 的浏览与控制需求

## 3. 本文范围

- local-first web control plane 的最小 runtime 形态
- browser UI 与 shared session/runtime seam 的连接方式
- workspace、session、artifact、evidence 的最小浏览与控制入口
- web 入口下的错误、恢复与权限提示路径
- web 入口对 execution / tool / provider 的调用边界

## 4. 非目标

- 不把 `WebEntry` 直接做成 remote SaaS control plane
- 不提前设计完整前端设计系统
- 不让浏览器直接持有私有 runtime services
- 不提前冻结多租户、远程协作或长期常驻 daemon 形态

## 5. 交付物

- 一个 local-first `WebEntry` 最小控制面骨架
- 一条 web 到 `SessionApi` 的稳定调用路径
- 一组 workspace / session / artifact / evidence 的最小观察面
- 一组浏览器入口下的错误恢复与状态提示规则
- 给 `17` 复用的 shared profile / authority 接入前提

## 6. 实施任务拆解

### 6.1 冻结 `WebEntry` 的 local-first 边界

- 明确 web control plane 默认跑在本地 runtime 旁边。
- 明确浏览器只是 UI 与控制入口，不拥有独立 runtime authority。
- 避免把 web 提前升级成需要远程编排、租户与控制面基础设施的形态。

### 6.2 把浏览器请求统一送进 `SessionApi`

- 明确创建、恢复、提交步骤、审批请求等 web 动作如何映射到 `SessionApi`。
- 保证 web 入口不会绕开 `SessionApi` 直接触碰 `Session` 或 `ExecutionLayer`。
- 让 web 与 CLI / host bridge 共用同一条 bootstrap / session 主链。

### 6.3 暴露最小观察与控制面

- 暴露当前 workspace、profile、session 的最小状态读取面。
- 暴露 artifact / evidence / lineage 的最小浏览面。
- 暴露受治理约束的最小动作入口，而不是在 UI 里偷偷越权。

### 6.4 收紧 web 与 execution 的边界

- 明确 web 只能通过共享 runtime seam 触发 execution。
- 明确 provider / tool execution 仍然由统一 execution layer 承担。
- 明确浏览器展示偏好不等于 provider authority。

### 6.5 做最小验证闭环

- 验证 web 入口可以稳定绑定 workspace 并恢复 session。
- 验证 web 不复制私有 session / execution 流程。
- 验证 local-first web shell 可以复用 CLI 与 host bridge 已有的共享对象与主链。

## 7. 依赖与并行建议

- 依赖 `13`、`14`、`15`
- 应在 `17` 前完成，先把三类入口 family 都收进同一条入口主链
- UI 细化与前端体验可以后置，但 shared runtime seam 必须先稳定

## 8. 验收与验证

完成这篇任务后，应能验证：

- `WebEntry` 已作为 local-first control plane 被切成可执行任务
- web 入口复用了同一条 `GarageLauncher -> SessionApi` 主链
- 浏览器入口不会复制第二套 runtime
- workspace / session / evidence 的最小观察面已经有稳定挂点

## 9. 完成后进入哪一篇

- `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
- `docs/tasks/T220-garage-webentry-streaming-and-live-updates.md`
- `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md`
- `docs/tasks/T222-garage-webentry-governance-and-review-surfaces.md`
