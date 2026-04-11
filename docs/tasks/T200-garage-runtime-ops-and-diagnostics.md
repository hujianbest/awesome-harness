# T200: Garage Runtime Ops And Diagnostics

- Task ID: `T200`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为 `Garage` 补 runtime ops baseline、structured logs、diagnostics 与 local health surface，使独立运行形态在出现问题时可检查、可定位、可解释。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/tasks/T180-garage-secrets-and-credential-resolution.md`
  - `docs/tasks/T190-garage-distribution-and-install-layout.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`
  - `docs/features/F050-governance-model.md`

## 1. 任务目标

这一篇解决的是：

- Garage 出问题时怎么查
- runtime 运行状态如何被健康化、结构化与最小可观测
- CLI、宿主桥与 WebEntry 如何共享同一套 diagnostics 语义

## 2. 输入设计文档

这一篇主要承接：

- authority、secrets 与 install layout 已形成运行前提
- execution layer 已有统一 trace / event 语义
- governance、workspace surfaces 与 evidence 已是共享真相面

## 3. 本文范围

- structured logs
- diagnostics objects 与 health surface
- runtime bootstrap、profile resolution、session、execution 的最小观测面
- redaction 与 operator-safe 输出规则
- 给 Web observability 与 trace ops surface 复用的基础设施

## 4. 非目标

- 不实现重型 observability 平台
- 不一次性引入分布式 tracing stack
- 不让 ops surface 反向成为新的 authority 层
- 不提前设计多租户运维控制面

## 5. 交付物

- 一套 runtime ops baseline
- 一组结构化日志与 diagnostics 语义
- 一条 local health / status surface
- 给 `T201`、`T221` 与 `T230` 复用的观测基础

## 6. 实施任务拆解

### 6.1 冻结 structured logs 与 diagnostics 语义

- 明确 bootstrap、authority resolution、session、execution、governance 的最小日志事件。
- 明确面向 operator 的 diagnostics 对象与字段。
- 保持 diagnostics 可读、可过滤、可被后续 UI 消费。

### 6.2 补齐 redaction 与安全输出

- secrets、credentials 与敏感 provider 配置默认不进入明文日志。
- 明确 diagnostics 中哪些字段只显示引用或摘要。
- 避免为了排错破坏 authority 与 security 边界。

### 6.3 暴露 local health surface

- 暴露 runtime 当前 profile、workspace、session、entry surface 与关键组件状态。
- 明确什么算 healthy、degraded、blocked。
- 让 CLI、Web 与宿主桥都能复用同一 health 语义。

### 6.4 接入 distribution 与 release

- 让 distribution 安装态也能稳定产出同一套 diagnostics。
- 让 release smoke 复用 health / diagnostics 判断。
- 避免“开发态可观测、安装态不可观测”的分叉。

### 6.5 做最小验证闭环

- 验证主要失败路径都能得到结构化 diagnostics。
- 验证 redaction 不破坏问题定位能力。
- 验证 ops baseline 能为后续 trace surface 与 web observability 提供稳定输入。

## 7. 依赖与并行建议

- 依赖 `17`、`18`、`20`
- 应先于 `23`、`28` 与 `30`
- 可与具体宿主 adapter 细化并行，但统一 diagnostics 语义应先稳定

## 8. 验收与验证

完成这篇任务后，应能验证：

- Garage 已有统一 runtime ops baseline
- 问题定位不再依赖临时打印和入口私有诊断
- secrets 与 authority 在 observability 下仍被保护
- trace surface、Web observability 与 optional orchestration 已有统一输入

## 9. 完成后进入哪一篇

- `docs/tasks/T201-garage-execution-trace-and-evidence-ops-surface.md`
- `docs/tasks/T221-garage-webentry-observability-and-traces-ui.md`
