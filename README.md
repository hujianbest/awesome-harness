# Garage

`Garage` 是一个面向 `solo creator` 的、`local-first`、`workspace-first` 的 agent runtime。
它想做的不是另一个聊天壳，而是一套能组织 AI 团队、沉淀 evidence、在治理下持续成长的 `Creator OS` 骨架。

当前仓库是 `Garage` 的开源主仓。现阶段它同时扮演：

- `Garage Source Root`
- 当前默认的 dogfooding workspace
- reference packs、runtime scaffolding 和 docs truth sources 的承载面

## 当前状态

这个项目已经可以被“运行”，但还不是一个已经打包好的 end-user app。

今天仓库里已经有：

- `src/` 下的 runtime topology、bootstrap 和 execution layer 骨架
- `Product Insights Pack` 和 `Coding Pack` 两个 reference packs 的 contract surface
- `artifacts/`、`evidence/`、`sessions/`、`archives/`、`.garage/` 这套 file-backed workspace surfaces
- 用 `unittest` 维护的最小回归验证

今天还没有：

- 稳定的 `garage` CLI 命令
- GUI / IDE product surface
- installer / daemon / 多 workspace supervisor
- 完整 provider 配置、secrets 管理和生产级 execution backends

如果你是第一次进入这个仓库，最重要的判断是：

**当前最靠谱的运行方式，是把它当成一个 Python runtime scaffold + docs-first open-source project 来运行，而不是把它当成已经交付完成的桌面应用或 SaaS。**

## 环境要求

- `Python 3.12+`
- 可选：`PyYAML`
  只在维护 `.agents/skills/skill-creator/` 下的脚本时需要

## 快速开始

1. 克隆仓库并进入根目录。
2. 让 Python 能导入 `src/` 下的运行时代码。

PowerShell:

```powershell
$env:PYTHONPATH = "src"
```

bash / zsh:

```bash
export PYTHONPATH=src
```

## 当前项目怎么运行

### 1. 运行测试套件

这是当前最直接的“项目是否能跑起来”的验证方式：

```bash
python -m unittest discover -s tests
```

这会验证当前已经落下来的实现切片，包括：

- runtime topology bindings
- unified bootstrap chain
- session create / resume / attach
- reference pack registry loading
- provider / tool execution skeleton

### 2. 运行一个最小 bootstrap demo

如果你想真的“启动一次 Garage runtime”，可以直接在 Python 里调用 `GarageLauncher`。

下面这个例子会：

- 使用当前仓库作为 `source root`
- 在临时目录里创建 `runtime home`
- 在临时目录里创建外部 `workspace`
- 加载 `packs/` 下的 reference packs
- 创建一个新的 `coding` session
- 把 session state 落到 workspace surface

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from bootstrap import BootstrapConfig, GarageLauncher, LaunchMode

repo_root = Path.cwd()
launcher = GarageLauncher()

with TemporaryDirectory() as tmp:
    tmp_root = Path(tmp)
    result = launcher.launch(
        BootstrapConfig(
            launch_mode=LaunchMode.CREATE,
            source_root=repo_root,
            runtime_home=tmp_root / "runtime-home",
            workspace_root=tmp_root / "workspace",
            workspace_id="garage-demo",
            profile_id="default",
            entry_surface="cli",
            problem_kind="implementation",
            entry_pack="coding",
            entry_node="coding.bridge-intake",
            goal="Bootstrap a demo Garage session.",
        )
    )

    print(result.session_state.session_id)
    print(result.session_state.session_status)
    print(result.session_route.file_path)
```

说明：

- 这个 demo 不需要 provider API key。
- 它验证的是当前的 topology、bootstrap、registry、governance 和 workspace surface 主链。
- 现在的 execution layer 已经有统一对象和测试，但还不是完整的生产级 provider runtime。

### 3. 以当前仓库作为 dogfooding workspace 运行

当前仓库处于 `source-coupled workspace mode`：

- 仓库根目录既是 `source root`
- 也是当前默认 dogfooding workspace

这意味着如果你故意把 repo root 当 workspace，用到的主事实面会是：

- `artifacts/`
- `evidence/`
- `sessions/`
- `archives/`
- `.garage/`

对开源贡献者来说，更推荐先用上面的“临时外部 workspace”例子，这样不会把 demo 状态混进你的 clone。

## 仓库结构

| 路径 | 作用 |
| --- | --- |
| `README.md` | 仓库级入口 |
| `AGENTS.md` | 仓库级 agent 约定 |
| `pyproject.toml` | Python package / `src` layout 入口 |
| `src/` | `Garage` runtime 的当前实现面 |
| `docs/` | 主文档树与 source-of-truth |
| `packs/` | 当前 reference packs |
| `tests/` | `unittest` 验证面 |
| `.agents/skills/` | 通用 skills 与 skill 工具链 |
| `artifacts/`、`evidence/`、`sessions/`、`archives/`、`.garage/` | workspace-first file-backed surfaces |

## 先读哪里

推荐阅读顺序：

1. `docs/README.md`
2. `docs/VISION.md`
3. `docs/GARAGE.md`
4. `docs/ROADMAP.md`
5. `docs/architecture/`
6. `docs/features/`
7. `docs/design/`
8. `docs/tasks/README.md`

如果你只关心“当前为什么这样运行”，优先看：

- `docs/features/F210-runtime-home-and-workspace-topology.md`
- `docs/features/F220-runtime-bootstrap-and-entrypoints.md`
- `docs/features/F230-runtime-provider-and-tool-execution.md`

## 开发与验证

当前仓库的实现约束：

- `Markdown-first`
- `file-backed`
- `Contract-first`
- `workspace-first`
- `one runtime, many entry surfaces`

当前没有统一 CI；最小回归入口是：

```bash
python -m unittest discover -s tests
```

## Skill 工具链

如果你要维护 `.agents/skills/` 下的 skills，可以进入 `.agents/skills/skill-creator/` 运行：

```bash
python -m scripts.quick_validate <skill-dir>
python -m scripts.package_skill <skill-dir> [output-dir]
python -m scripts.aggregate_benchmark <benchmark-dir>
python -m scripts.generate_report <json-input> [-o output.html]
python -m scripts.run_eval ...
python -m scripts.run_loop ...
```

注意：

- 这些脚本一般需要 `PyYAML`
- 部分评测命令还依赖 `claude` CLI
- 这套工具链是 skill 维护面，不等于 Garage end-user runtime

## 当前非目标

当前 README 不应让你误解这件事：

- `Garage` 还不是一个已经打磨完成的通用桌面产品
- 这个仓库也不是单纯的 workflow 资料库
- 目前最真实的状态，是一个 docs-first、runtime-first、open-source 演进中的 `Creator OS` 骨架
