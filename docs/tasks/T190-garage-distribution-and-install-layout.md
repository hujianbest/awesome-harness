# T190: Garage Distribution And Install Layout

- Task ID: `T190`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 把当前 repo-local dogfooding runtime 推进到可分发的安装布局、版本化与升级路径，使稳定 `garage` CLI 与 `runtime home` 真正具备安装与升级语义。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T140-garage-stable-cli-shell.md`
  - `docs/tasks/T170-garage-provider-profile-loader-and-authority-resolution.md`
  - `docs/tasks/T180-garage-secrets-and-credential-resolution.md`
  - `docs/tasks/T181-garage-runtime-home-config-doctor.md`
  - `docs/features/F210-runtime-home-and-workspace-topology.md`

## 1. 任务目标

这一篇解决的是：

- `Garage` 如何从源码仓运行，过渡到可分发安装形态
- CLI、runtime home 与 source root 在安装后如何布局
- 升级、回滚与兼容边界如何被明确

## 2. 输入设计文档

这一篇主要承接：

- `CLIEntry` 已成为第一条真实入口
- `runtime home` 已有 authority、secrets 与 doctor 语义
- source root / runtime home / workspace 三层拓扑需要在安装态继续成立

## 3. 本文范围

- 分发产物与 install layout
- CLI entrypoint、runtime home 默认位置与 versioning 语义
- 安装、升级、回滚与兼容边界
- source-coupled dogfooding 与独立安装态之间的关系
- distribution 面向 `T191` 的 smoke 前提

## 4. 非目标

- 不在这里实现完整发布流水线
- 不提前锁死所有平台包管理器
- 不提前引入 remote package registry
- 不把 installer 设计成新的 runtime authority 层

## 5. 交付物

- 一套可解释的 install layout 语义
- 一条稳定的 CLI 分发与版本化路径
- 一组升级 / 回滚 / 兼容规则
- 给 release smoke 与 ops 复用的安装基线

## 6. 实施任务拆解

### 6.1 冻结 install layout

- 明确可执行入口、package layout 与 runtime home 默认位置。
- 明确 source root 不再等于唯一运行形态。
- 保持 workspace-first surfaces 仍然位于目标 workspace，而不是被安装目录吞并。

### 6.2 定义版本化与升级边界

- 明确 binary / package version 与 runtime-home schema version 的关系。
- 明确何时允许就地升级，何时必须迁移或人工确认。
- 为回滚、备份与兼容提示预留统一语汇。

### 6.3 接入 CLI 与 authority 链

- 让稳定 CLI 分发形态能够定位 `RuntimeProfile`、runtime home 与 workspace。
- 让 distribution 复用 secrets / doctor / authority resolution 主线。
- 避免安装态再生成一套私有配置逻辑。

### 6.4 兼容 dogfooding 与独立安装

- 保留当前 repo-local dogfooding mode 的有效性。
- 明确独立安装态与 source-coupled 模式的边界和切换方式。
- 避免在安装设计里回退到“只能在源码仓运行”。

### 6.5 做最小验证闭环

- 验证安装布局不会破坏 workspace-first 与 runtime-home 分层。
- 验证 CLI、doctor 与 authority 在安装态下仍然一致。
- 验证升级与回滚路径对后续 release smoke 可测。

## 7. 依赖与并行建议

- 依赖 `14`、`17`、`18`、`19`
- 应先于 `21` 落地
- 可与具体宿主 adapter 设计并行，但 release 语义应先稳定

## 8. 验收与验证

完成这篇任务后，应能验证：

- Garage 已有稳定的安装布局与版本化语义
- 独立安装态不再依赖源码仓结构
- CLI 与 runtime home 在安装后仍共享同一 authority 链
- release smoke、ops 与具体入口深化已有可交付前提

## 9. 完成后进入哪一篇

- `docs/tasks/T191-garage-release-smoke-and-compatibility-matrix.md`
- `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
