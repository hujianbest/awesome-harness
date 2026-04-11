# T191: Garage Release Smoke And Compatibility Matrix

- Task ID: `T191`
- 状态: 待执行
- 日期: 2026-04-11
- 定位: 为可分发的 `Garage` 补 release smoke checks、兼容矩阵与最小发布门槛，使 CLI、runtime home 与主要宿主 / OS 组合在发布前有可重复验证面。
- 当前阶段: 完整架构主线下的第三组产品化 implementation tracks
- 关联设计文档:
  - `docs/tasks/T190-garage-distribution-and-install-layout.md`
  - `docs/tasks/T181-garage-runtime-home-config-doctor.md`
  - `docs/tasks/T140-garage-stable-cli-shell.md`
  - `docs/features/F220-runtime-bootstrap-and-entrypoints.md`

## 1. 任务目标

这一篇解决的是：

- 发布前最少要验证哪些东西
- 哪些 OS / host / install 组合属于当前支持矩阵
- 什么条件下可以说“这版 Garage 可以对外给人试”

## 2. 输入设计文档

这一篇主要承接：

- distribution 与 install layout 已冻结
- runtime home doctor 已能发现配置问题
- CLI 是第一条真实入口
- 未来还会有 HostBridge 与 WebEntry 的深化切片

## 3. 本文范围

- release smoke checklist
- 当前支持的 OS / install / host compatibility matrix
- 最小发布门槛与阻断条件
- smoke 失败、兼容回退与已知限制的表达方式
- 给具体宿主 adapter 与 optional orchestration 的验证前提

## 4. 非目标

- 不实现完整 CI/CD 平台
- 不在这里覆盖全部产品功能测试
- 不承诺尚未完成的具体宿主 adapter 已 fully supported
- 不把兼容矩阵伪装成长期不可变承诺

## 5. 交付物

- 一套 release smoke checklist
- 一张当前支持矩阵
- 一组 blocker / warning / experimental 标签语义
- 给 `T230` 与后续 release automation 复用的发布门槛

## 6. 实施任务拆解

### 6.1 冻结 smoke checklist

- 覆盖安装、启动、doctor、create / resume、authority resolution 与最小 execution path。
- 覆盖 workspace-first surfaces 是否能在安装态下正常工作。
- 保持 smoke 聚焦最小高价值路径，而不是膨胀成完整回归集。

### 6.2 定义兼容矩阵

- 明确当前支持或实验性的 OS、安装方式、入口 family 与宿主组合。
- 明确哪些矩阵格子是阻断、哪些只是待验证。
- 避免在具体宿主 adapter 完成前做过度承诺。

### 6.3 定义发布门槛

- 明确哪些 smoke 失败会阻断发布。
- 明确哪些 warning 可以带着已知限制发布。
- 明确版本说明里应暴露哪些兼容边界与非目标。

### 6.4 接入后续宿主与 orchestration 方向

- 为具体宿主 adapters 预留各自的 smoke 扩展位。
- 为可选 supervisor / daemon 预留单独矩阵，而不是混入基础发布门槛。
- 保持 release 基线优先围绕 CLI 与共享 runtime 主链。

### 6.5 做最小验证闭环

- 验证 smoke checklist 可以覆盖高风险断点。
- 验证兼容矩阵与当前任务树状态一致。
- 验证发布门槛不会假装支持尚未完成的产品面。

## 7. 依赖与并行建议

- 依赖 `19`、`20`
- 应先于 `23` 与 `30` 落地
- 与具体宿主 adapter 细化可并行，但基础发布门槛应先确立

## 8. 验收与验证

完成这篇任务后，应能验证：

- Garage 已有可复用的 release smoke 基线
- 当前支持矩阵可被明确陈述
- 发布门槛与任务成熟度对齐
- 后续具体宿主与 orchestration 已有清晰的验证入口

## 9. 完成后进入哪一篇

- `docs/tasks/T200-garage-runtime-ops-and-diagnostics.md`
- `docs/tasks/T230-garage-runtime-supervisor-and-multi-workspace-daemon.md`
