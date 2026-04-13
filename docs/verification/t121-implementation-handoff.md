## 实现交接块

- Task ID: T121
- 回流来源: 主链实现
- 触碰工件: `src/surfaces/__init__.py`, `src/surfaces/filebacked.py`, `tests/test_filebacked_surfaces.py`
- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch:
- 测试设计确认证据: `docs/approvals/test-design-approval-t121.md`
- RED 证据: `pytest tests/test_filebacked_surfaces.py` -> `ModuleNotFoundError: No module named 'surfaces'`
- GREEN 证据: `pytest tests/test_filebacked_surfaces.py` -> `2 passed`
- 与任务计划测试种子的差异: 无；覆盖 routing 正向与 unknown kind 负向
- 剩余风险 / 未覆盖项:
  - 尚未覆盖 artifact kind 到权限策略映射
- Pending Reviews And Gates: ahe-bug-patterns, ahe-test-review, ahe-code-review, ahe-traceability-review, ahe-regression-gate, ahe-completion-gate
- Next Action Or Recommended Skill: ahe-bug-patterns
