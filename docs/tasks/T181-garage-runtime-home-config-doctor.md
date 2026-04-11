# T181: Garage Runtime Home Config Doctor

- Task ID: `T181`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为 `runtime home` 补 config validation、doctor UX 与安全迁移钩子，使 profile / config / adapters 在进入真实执行前就能被发现、诊断与解释。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/tasks/T180-garage-secrets-and-credential-resolution.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`

## 1. 任务目标

这一篇解决的是：

- runtime home 配置有问题时，用户如何在执行前就知道
- profile / config / adapters 目录怎样被主动检查
- 配置升级与迁移如何保持可解释，而不是静默破坏运行

## 2. 输入设计文档

这一篇主要承接：

- `runtime home` 的最小目录语义
- `RuntimeProfile` 与 provider authority resolution
- secrets / credential references 的最小语汇
- 三类入口共享同一 runtime 配置主线

## 3. 本文范围

- runtime home 目录完整性检查
- config schema / reference / compatibility doctor
- profile 缺失、adapter 失配、credential reference 失效的诊断面
- 迁移前检查、版本提示与安全修复建议
- CLI / Web / HostBridge 共用的 doctor 输出语义

## 4. 非目标

- 不在这里实现完整 installer
- 不把 doctor 做成远程管理平台
- 不自动替用户执行高风险迁移
- 不让 doctor 反向拥有配置 authority

## 5. 交付物

- 一套 runtime-home doctor 检查清单
- 一组稳定的 doctor 输出分类与 severity 语义
- 一套安全迁移钩子与变更前检查规则
- 给 distribution、release 与 ops 复用的配置诊断前提

## 6. 实施任务拆解

### 6.1 冻结 doctor 检查面

- 检查 `profiles/`、`config/`、`adapters/`、必要 sidecars 与引用完整性。
- 检查 profile 与 adapter 是否能被同一 authority 链解释。
- 避免把运行时异常都推迟到真正执行时才发现。

### 6.2 统一 doctor 输出语义

- 明确 error、warning、migration-needed、unsupported 等结果分类。
- 明确哪些问题阻断启动，哪些只给提示。
- 让 CLI、Web 与宿主桥都能复用同一组诊断对象。

### 6.3 补齐安全迁移钩子

- 为 runtime home 结构升级预留 migrate / preview / backup-required 语义。
- 明确什么时候允许自动修复，什么时候必须人工确认。
- 避免升级时静默改写 authority 真相。

### 6.4 接入入口与分发链

- 让 `CLIEntry` 能在启动前跑 doctor。
- 让 release smoke 与 distribution 流程复用 doctor 检查。
- 让具体宿主 adapters 只消费 doctor 结果，不各自定义兼容检查。

### 6.5 做最小验证闭环

- 验证目录缺失、字段失配、credential reference 失效可以被稳定发现。
- 验证 doctor 输出对人类和系统都可读。
- 验证迁移建议不会越权修改当前 authority。

## 7. 依赖与并行建议

- 依赖 `17`、`18`
- 应先于 `20`、`21` 落地
- 与 ops 设计有关，但 doctor 语义应先于更重的 observability 展开

## 8. 验收与验证

完成这篇任务后，应能验证：

- runtime home 已有统一 doctor 与配置诊断面
- 入口与 release 流程不再依赖隐式配置成功
- 迁移与兼容问题可以在执行前被发现
- distribution 与 ops 已有稳定的配置检查前提

## 9. 完成后进入哪一篇

- `docs/tasks/T190-garage-distribution-and-install-layout.md`
- `docs/tasks/T191-garage-release-smoke-and-compatibility-matrix.md`
