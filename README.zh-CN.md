# Garage

[English](README.md) | **中文**

`Garage` 是一个面向 `solo creator` 的开源 `Agent Teams` 工作环境。

它遵循一个核心原则：**one runtime, many entry surfaces**。

- CLI、Web、HostBridge 共用同一套 runtime truth
- runtime/governance/continuity/contracts/packs 以可组合 Python 模块实现
- 仓库通过任务、评审、门禁、批准工件驱动开发流程

当前状态：已具备可运行的开发基线与完整自动化任务证据链，但还不是生产级发布版本。

## Quick Install

环境要求：

- `Python 3.12+`

安装当前开发版：

```bash
python -m pip install -e .
```

安装完成后可用：

```bash
garage --help
```

如果你希望在未安装时，直接从仓库里导入 Python 模块：

```bash
export PYTHONPATH=src
```

PowerShell：

```powershell
$env:PYTHONPATH = "src"
```

## Quick Start

创建 session：

```bash
garage create --team garage --workspace default --profile dev
```

恢复一个已有 session：

```bash
garage resume --session <session-id>
```

附着 workspace：

```bash
garage attach --session <session-id> --workspace default
```

提交一步：

```bash
garage step --session <session-id> --input "hello"
```

查询状态：

```bash
garage status --session <session-id>
```

运行测试：

```bash
pytest
```

## 已实现能力

- **入口层**
  - CLI 入口（`create/resume/attach/step/status`）
  - Web control-plane 基线与 web-depth guardrails
  - HostBridge handoff/rework seam
- **Runtime 核心**
  - runtime home/profile authority 基线
  - session lifecycle runtime core
  - execution authority + trace/evidence 引用
- **Workspace Truth 与 Governance**
  - workspace surfaces 的 file-backed artifact routing
  - governance gate 判定与 evidence 引用输出
- **Continuity 与 Growth**
  - continuity stores（memory/skills buckets）
  - growth proposal 生命周期（`accepted/rejected/deferred`）
- **Contracts/Registry/Packs**
  - shared contract validation
  - registry discovery
  - reference pack metadata catalog
- **Hardening 与 Ops**
  - credential resolution 基线
  - runtime home doctor 基线
  - runtime diagnostics event ops

## 当前限制

- 面向终端用户的完整发布版
- 完整 Web 产品深度与 UX 打磨
- 全部 runtime stores 的持久化实现
- 更高级 provider backend 与 secrets 分层来源
- daemon/supervisor/multi-workspace orchestration
- 分布式或远程控制面

## Documentation

建议从这里开始：

- `docs/README.md`
- `docs/VISION.md`
- `docs/GARAGE.md`
- `docs/ROADMAP.md`

架构与特性真相：

- `docs/architecture/1-garage-system-overview.md`
- `docs/architecture/2-garage-runtime-reference-model.md`
- `docs/architecture/10-entry-and-host-injection-layer.md`
- `docs/features/F10-agent-teams-product-surface.md`
- `docs/features/F11-runtime-topology-and-entry-bootstrap.md`
- `docs/features/F16-execution-and-provider-tool-plane.md`

设计与任务：

- `docs/design/`
- `docs/tasks/README.md`
- `docs/tasks/2026-04-13-garage-mainline-tasks.md`
- `docs/tasks/2026-04-13-garage-mainline-task-board.md`

仓库结构：

| 路径 | 用途 |
| --- | --- |
| `src/` | runtime/entry/governance/continuity/contracts/packs 实现 |
| `tests/` | 基于 pytest 的回归测试 |
| `docs/reviews/` | 评审阶段证据记录 |
| `docs/verification/` | 门禁/finalize 证据记录 |
| `docs/approvals/` | 批准步骤记录（含 auto 模式） |
| `docs/tasks/` | 任务计划与队列投影 |
| `task-progress.md` | 当前 workflow 状态快照 |

## Contributing

`Garage` 仍在持续演进，当前高价值贡献包括：

- 强化共享 runtime seams
- 改进任务/评审/门禁证据质量
- 扩展失败路径与可恢复性测试覆盖
- 保持 docs/features/design/tasks 一致性

一个基础的贡献者流程：

```bash
git clone <your-fork-or-repo-url>
cd Garage
python -m pip install -e .
pytest
```

做较大改动前，建议先读：

- `AGENTS.md`
- `docs/README.md`
- `docs/architecture/`
- `docs/features/`
- `docs/tasks/README.md`

这个项目是 documentation-led：`docs/architecture/`、`docs/features/`、`docs/design/` 定义系统真相，`docs/tasks/` 定义可执行交付切片。
