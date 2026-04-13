# Garage

**English** | [中文](README.zh-CN.md)

`Garage` is an open-source `Agent Teams` workspace for a `solo creator`.

It follows one core principle: **one runtime, many entry surfaces**.

- CLI, Web, and HostBridge share one runtime truth.
- Runtime/gov/continuity/contracts/packs capabilities are implemented as composable Python modules.
- The repository is workflow-driven with explicit task, review, gate, and approval artifacts.

Current status: developer-grade working baseline with full automated task-chain evidence, not a production release.

## Quick Install

Requirements:

- `Python 3.12+`

Install the current development build:

```bash
python -m pip install -e .
```

After installation:

```bash
garage --help
```

If you want Python imports to work directly from the repository without installation:

```bash
export PYTHONPATH=src
```

PowerShell:

```powershell
$env:PYTHONPATH = "src"
```

## Quick Start

Create a session:

```bash
garage create --team garage --workspace default --profile dev
```

Resume a session:

```bash
garage resume --session <session-id>
```

Attach a workspace:

```bash
garage attach --session <session-id> --workspace default
```

Submit one step:

```bash
garage step --session <session-id> --input "hello"
```

Check session status:

```bash
garage status --session <session-id>
```

Run tests:

```bash
pytest
```

## Implemented Capabilities

- **Entry Surfaces**
  - CLI entry (`create/resume/attach/step/status`)
  - Web control-plane baseline and web-depth guardrails
  - HostBridge handoff/rework seam
- **Runtime Core**
  - Runtime home/profile authority baseline
  - Session lifecycle runtime core
  - Execution authority + trace/evidence references
- **Workspace Truth and Governance**
  - File-backed artifact routing for workspace surfaces
  - Governance gate decision runtime with evidence refs
- **Continuity and Growth**
  - Continuity stores (memory/skills buckets)
  - Growth proposal lifecycle (`accepted/rejected/deferred`)
- **Contracts, Registry, and Packs**
  - Shared contract validation
  - Registry discovery
  - Reference pack catalog metadata
- **Hardening and Ops**
  - Credential resolution baseline
  - Runtime home doctor baseline
  - Runtime diagnostics event ops

## Known Limits

- a production-ready packaged release
- full web UX/product depth
- durable persistence for all runtime stores
- advanced provider backends and secret source hierarchy
- daemon/supervisor/multi-workspace orchestration
- distributed or remote control plane

## Documentation

Start with:

- `docs/README.md`
- `docs/VISION.md`
- `docs/GARAGE.md`
- `docs/ROADMAP.md`

Architecture and feature truth:

- `docs/architecture/1-garage-system-overview.md`
- `docs/architecture/2-garage-runtime-reference-model.md`
- `docs/architecture/10-entry-and-host-injection-layer.md`
- `docs/features/F10-agent-teams-product-surface.md`
- `docs/features/F11-runtime-topology-and-entry-bootstrap.md`
- `docs/features/F16-execution-and-provider-tool-plane.md`

Design and tasks:

- `docs/design/`
- `docs/tasks/README.md`
- `docs/tasks/2026-04-13-garage-mainline-tasks.md`
- `docs/tasks/2026-04-13-garage-mainline-task-board.md`

Repository structure:

| Path | Purpose |
| --- | --- |
| `src/` | runtime/entry/governance/continuity/contracts/packs implementation |
| `tests/` | pytest-based regression coverage |
| `docs/reviews/` | review-stage evidence records |
| `docs/verification/` | gate/finalize evidence records |
| `docs/approvals/` | approval-step records (including auto mode approvals) |
| `docs/tasks/` | task plans and queue projection artifacts |
| `task-progress.md` | current workflow state snapshot |

## Contributing

`Garage` is still evolving. High-value contributions are:

- hardening runtime seams
- improving task/review/gate evidence quality
- extending test coverage around failure paths and recoverability
- keeping docs/features/design/tasks consistent

Basic flow:

```bash
git clone <your-fork-or-repo-url>
cd Garage
python -m pip install -e .
pytest
```

Before large changes, read:

- `AGENTS.md`
- `docs/README.md`
- `docs/architecture/`
- `docs/features/`
- `docs/tasks/README.md`

The project is documentation-led: architecture/features/design define system truth, and tasks define executable delivery slices.
