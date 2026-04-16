# F002 设计文档: Garage Live — 引擎接入真实宿主

- 状态: 草稿
- 日期: 2026-04-16
- 关联规格: docs/features/F002-garage-live.md
- 关联 Phase 1 设计: docs/designs/2026-04-15-garage-agent-os-design.md

## 1. 概述

F002 的核心任务是把 Phase 1 的"空壳引擎"变成"能跑的引擎"。改动量不大——补全 ClaudeCodeAdapter 的真实调用 + 添加 CLI 入口 + 串起自动 experience 记录。

## 2. 设计决策

### D-201: CLI 框架选择

**选择**: Python 标准库 `argparse`

**理由**: Phase 1 技术栈就是纯 Python 标准库 + dataclass，不引入新依赖。argparse 足够支撑 4 个子命令。

**不选择**: click、tycoon、rich-click — 过度依赖，Phase 3 再考虑。

### D-202: Claude Code 调用方式

**选择**: `subprocess.run(["claude", "-p", prompt])` 同步调用

**理由**:
- Claude Code 的 print mode (`-p`) 是非交互的，适合被程序调用
- 同步调用简单，避免 asyncio 复杂度
- 设置合理的 timeout（默认 300s）

**prompt 构造**:
```
你正在执行 {skill_name} skill。以下是 skill 的完整定义：

{SKILL.md 内容}

请根据以上 skill 定义执行任务。工作目录: {workspace_root}
```

### D-203: CLI 入口点

**选择**: `pyproject.toml` 的 `[project.scripts]` 定义 `garage` 命令

```toml
[project.scripts]
garage = "garage_os.cli:main"
```

安装后直接可用 `garage init`、`garage run` 等。

### D-204: Session 自动生命周期

`garage run` 的执行流程：

```
1. garage run <skill-name>
2. SessionManager.create() → 新 session (idle)
3. StateMachine.transition(idle → running)
4. ClaudeCodeAdapter.invoke_skill(skill_name)
5. 如果成功:
   - StateMachine.transition(running → completed)
   - ExperienceIndex.store() → 记录 experience
   - ArtifactBoardSync.sync() → 验证 artifact 一致性
   - SessionManager.archive()
6. 如果失败:
   - ErrorHandler.classify_error() → 分类错误
   - StateMachine.transition(running → failed)
   - 记录错误到 experience
```

### D-205: 测试策略

| 组件 | 测试方式 |
|------|----------|
| CLI 命令 | `subprocess` 调用测试，或直接调用 `main()` 函数 |
| ClaudeCodeAdapter 真实调用 | mock `subprocess.run`，验证命令构造 |
| Session 生命周期 | 与 Phase 1 一致，用 tmp_path |
| Experience 记录 | 验证写入 `.garage/experience/records/` 的 JSON |
| 全量回归 | `uv run pytest tests/ -q` 保持 416+ 通过 |

## 3. 模块设计

### 3.1 CLI 模块 (`src/garage_os/cli.py`)

```python
def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(prog="garage")
    subparsers = parser.add_subparsers(dest="command")

    # garage init
    init_parser = subparsers.add_parser("init")

    # garage status
    status_parser = subparsers.add_parser("status")

    # garage run <skill-name>
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("skill_name")
    run_parser.add_argument("--timeout", type=int, default=300)

    # garage knowledge search <query>
    knowledge_parser = subparsers.add_parser("knowledge")
    knowledge_sub = knowledge_parser.add_subparsers(dest="action")
    search_parser = knowledge_sub.add_parser("search")
    search_parser.add_argument("query")
    list_parser = knowledge_sub.add_parser("list")

    args = parser.parse_args()
    # dispatch to handler...
```

### 3.2 ClaudeCodeAdapter 补全

当前 `invoke_skill()` 只读 SKILL.md 返回内容。需要改为：

```python
def invoke_skill(self, skill_name: str, params: dict | None = None) -> dict:
    # 1. 读取 SKILL.md
    skill_path = self.workspace_root / ".agents/skills" / skill_name / "SKILL.md"
    skill_content = skill_path.read_text()

    # 2. 构造 prompt
    prompt = f"你正在执行 {skill_name} skill。\n\n{skill_content}"

    # 3. 调用 claude -p
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True,
        timeout=self.timeout,
        cwd=str(self.workspace_root),
    )

    # 4. 返回结果
    return {
        "output": result.stdout,
        "exit_code": result.returncode,
        "success": result.returncode == 0,
    }
```

### 3.3 Experience 自动记录

在 `garage run` 完成后，自动创建 experience record：

```python
ExperienceIndex(store_dir).store(ExperienceRecord(
    record_id=str(uuid.uuid4()),
    session_id=session_id,
    task_type=skill_name,
    domain="coding",
    skill_ids=[skill_name],
    key_patterns=[],
    outcome="success" if success else "failure",
    lessons_learned=result["output"][:500],  # 取前500字符
    duration_seconds=elapsed,
    timestamp=datetime.now(),
))
```

## 4. 文件影响

| 文件 | 操作 | 描述 |
|------|------|------|
| `src/garage_os/cli.py` | 新建 | CLI 入口 |
| `src/garage_os/adapter/claude_code_adapter.py` | 修改 | invoke_skill 改用 subprocess |
| `pyproject.toml` | 修改 | 添加 [project.scripts] |
| `tests/test_cli.py` | 新建 | CLI 测试 |
| `tests/adapter/test_host_adapter.py` | 修改 | 更新适配器测试 |

## 5. 任务拆分预估

| 任务 | 估计 | 依赖 |
|------|------|------|
| CLI 框架 + init/status | 2h | Phase 1 |
| ClaudeCodeAdapter 真实调用 | 1h | Phase 1 |
| garage run + session 生命周期 | 2h | CLI + Adapter |
| Experience 自动记录 | 1h | garage run |
| knowledge search CLI | 1h | Phase 1 |
| E2E demo 验证 | 1h | 全部 |

**总计：约 8h / 6 个任务**
