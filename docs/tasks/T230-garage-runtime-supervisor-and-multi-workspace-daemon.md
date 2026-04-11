# T230: Garage Runtime Supervisor And Multi-workspace Daemon

- Task ID: `T230`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 只在确有需求时，再把 `Garage` 推进到 supervisor / daemon / multi-workspace orchestration 形态，避免在 local-first、单 runtime 还未稳定时过早引入重型控制面复杂度。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T191-garage-release-smoke-and-compatibility-matrix.md`
  - `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
  - `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`

## 1. 任务目标

这一篇不是默认必做，而是解决一个后置问题：

- 当单进程、单 workspace、local-first runtime 已经稳定之后，是否需要补 supervisor / daemon / multi-workspace orchestration

它要证明的是：

- 如果要进到更重 orchestration，也仍然复用同一个 runtime 主线
- orchestration 只是包装 shared runtime，而不是重新定义系统真相

## 2. 输入设计文档

- install layout、release smoke 与 ops baseline 已经稳定
- WebEntry 已有 observability 面
- source root / runtime home / workspace 分层仍是基础约束

## 3. 本文范围

- supervisor / daemon 的最小存在理由
- multi-workspace orchestration 的最小边界
- 常驻进程、生命周期与健康管理
- 对 CLI / Web / HostBridge 的影响边界
- 进入实施前的 defer / go 条件

## 4. 非目标

- 不默认把 Garage 升级成 remote SaaS control plane
- 不提前引入分布式 worker mesh
- 不把多 workspace orchestration 当成当前主线前置条件
- 不让 daemon 反向吞并 workspace-first 与 authority 边界

## 5. 交付物

- 一套 supervisor / daemon 的进入条件
- 一条最小 orchestration 责任边界
- 一组 multi-workspace 风险、收益与 defer 规则
- 给后续更重控制面切片复用的前置判断

## 6. 实施任务拆解

### 6.1 明确为什么需要 orchestration

- 明确哪些真实场景要求常驻 runtime 或 multi-workspace coordination。
- 区分“便利性愿望”和“必须进入更重架构”的信号。

### 6.2 冻结 daemon / supervisor 边界

- 明确 supervisor 管什么，仍然不管什么。
- 保证它不替代 `Bootstrap`、`SessionApi`、`ExecutionLayer` 或 workspace facts。

### 6.3 评估 multi-workspace 语义

- 明确多 workspace 下 session、authority、health 与 diagnostics 的边界。
- 保持 `runtime home` 与 workspace 分层不被打破。

### 6.4 设定 defer / go 条件

- 只有当 release、ops、observability 与入口主线稳定后，才允许推进。
- 明确如果这些前置条件不成立，就继续 defer，而不是硬做。

### 6.5 做最小验证闭环

- 验证 orchestration 不会破坏 one runtime, many entry surfaces。
- 验证 multi-workspace 不会反向吞并 workspace-first 边界。

## 7. 依赖与并行建议

- 依赖 `21`、`22`、`28`
- 默认后置
- 不应在第三组产品化切片前段并行推进

## 8. 验收与验证

完成这篇任务后，应能验证：

- Garage 何时该进入更重 orchestration 已有清晰门槛
- daemon / supervisor 不会反向定义系统真相
- multi-workspace 的风险与边界已被明确

## 9. 完成后进入哪一篇

- 进入更重的 runtime orchestration / deployment / control-plane 任务切片，若后续确有需要
