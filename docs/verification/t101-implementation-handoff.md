## 实现交接块

- Task ID: T101
- 回流来源: 主链实现
- 触碰工件: `src/bootstrap/__init__.py`, `src/bootstrap/session_api.py`, `src/bootstrap/cli.py`, `tests/test_cli.py`
- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch:
- 测试设计确认证据: `docs/approvals/test-design-approval-t101.md`
- RED 证据: `pytest tests/test_cli.py` -> `ModuleNotFoundError: No module named 'bootstrap.cli'`（证明 CLI 入口缺失，符合预期失败）
- GREEN 证据: `pytest tests/test_cli.py` -> `3 passed`（create/resume/attach/step 路径通过）
- 与任务计划测试种子的差异: 无本质差异，按 T101 种子覆盖了正向链路和关键负向路径
- 剩余风险 / 未覆盖项:
  - 当前为内存态 SessionApi，尚未覆盖持久化恢复与跨进程场景
  - 尚未覆盖 CLI `status` 的端到端行为断言
- Pending Reviews And Gates: ahe-bug-patterns, ahe-test-review, ahe-code-review, ahe-traceability-review, ahe-regression-gate, ahe-completion-gate
- Next Action Or Recommended Skill: ahe-bug-patterns
