# T180: Garage Secrets And Credential Resolution

- Task ID: `T180`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把 `RuntimeProfile`、`runtime home` 与 adapters 需要的 secrets / credential references 收敛成统一 resolution seam，避免 `CLIEntry`、`HostBridgeEntry`、`WebEntry` 各自长自己的凭据读取逻辑。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`
  - `docs/features/F230-runtime-provider-and-tool-execution.md`
  - `docs/features/F050-governance-model.md`
  - `docs/architecture/A120-garage-core-subsystems-architecture.md`

## 1. 任务目标

在 `T170` 已冻结 profile authority 后，这一篇继续解决：

- provider / model / adapter 需要的 credential 到底从哪里来
- credential references 如何被统一解析
- 不同入口如何共享同一条 secrets resolution 主线

## 2. 输入设计文档

这一篇主要承接：

- `RuntimeProfile` 是 provider / model authority 主入口
- `runtime home` 承载 `profiles / config / adapters`
- host 只能提交 hint，不能重写 authority
- execution layer 只消费统一归一化配置对象

## 3. 本文范围

- secrets / credential references 的最小表达方式
- env、runtime home references 与 adapter-local references 的解析顺序
- 缺失、冲突、未授权时的错误面
- redaction、引用传递与最小可见范围
- 三类入口 family 的共享读取方式

## 4. 非目标

- 不一次性实现完整 secrets vault
- 不绑定特定云厂商或第三方 secret manager
- 不让 workspace 主事实面承载长期凭据真相
- 不把 host 自己的私有 secret store 直接变成 authority

## 5. 交付物

- 一套统一 credential reference 语汇
- 一条稳定的 secrets / credential resolution 顺序
- 一组 redaction 与错误返回规则
- 给 `T190`、`T200`、`T210-T212` 复用的 credential seam

## 6. 实施任务拆解

### 6.1 冻结 credential reference 语汇

- 明确 profile、config 与 adapter metadata 如何引用 secrets。
- 明确哪些值允许明文，哪些只能通过 reference 间接解析。
- 保持 credential 语义属于 runtime 配置层，而不是 pack 合同层。

### 6.2 统一 resolution 顺序

- 明确先读 `RuntimeProfile` 与 runtime 配置引用。
- 明确 env、runtime-home config 与 adapter-local metadata 的优先级。
- 避免不同入口 family 得到不同 credential 解析结果。

### 6.3 收紧错误与 redaction

- credential 缺失、冲突、引用失效时必须显式报错。
- logs、diagnostics 与 traces 中默认 redact secrets。
- 避免通过错误消息或 evidence 泄露敏感值。

### 6.4 接入 execution 与 adapters

- 让 execution layer 消费的是已解析、已归一化、已 redacted 的运行配置对象。
- 让具体 adapters 通过统一 seam 获取 credentials，而不是自己再读系统环境。
- 保证 host hint 仍然不能越过 authority 改写 secrets 来源。

### 6.5 做最小验证闭环

- 验证三类入口共享同一 credential resolution 结果。
- 验证缺失和冲突可以被稳定诊断。
- 验证 secrets 不会进入 workspace-first 主事实面。

## 7. 依赖与并行建议

- 依赖 `17`
- 应先于 `20`、`22` 与具体宿主 adapters 落地
- 与 `19` 可并行设计，但最终 doctor 规则要服从本篇 resolution 语义

## 8. 验收与验证

完成这篇任务后，应能验证：

- credentials 已有统一 runtime 解析语义
- 三类入口不会再各自发明 secret 读取逻辑
- secrets 不会悄悄漂移进 workspace facts 或 host 私货
- 后续 distribution、ops 与 host adapters 已有稳定凭据前提

## 9. 完成后进入哪一篇

- `docs/tasks/T181-garage-runtime-home-config-doctor.md`
- `docs/tasks/T190-garage-distribution-and-install-layout.md`
- `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
