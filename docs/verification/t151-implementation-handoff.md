## 实现交接块

- Task ID: T151
- 回流来源: 主链实现
- 触碰工件: `src/bootstrap/credential_resolution.py`, `src/bootstrap/runtime_home_doctor.py`, `tests/test_credential_resolution.py`, `tests/test_runtime_home_doctor.py`
- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch:
- 测试设计确认证据: `docs/approvals/test-design-approval-t151.md`
- RED 证据: `pytest tests/test_credential_resolution.py tests/test_runtime_home_doctor.py` -> missing module import failures
- GREEN 证据: `pytest tests/test_credential_resolution.py tests/test_runtime_home_doctor.py` -> `4 passed`
- 与任务计划测试种子的差异: 无；覆盖 credential resolve 正向、missing credential 负向和 doctor warn 路径
- 剩余风险 / 未覆盖项:
  - 尚未覆盖多 provider secret fallback 顺序
- Pending Reviews And Gates: ahe-bug-patterns, ahe-test-review, ahe-code-review, ahe-traceability-review, ahe-regression-gate, ahe-completion-gate
- Next Action Or Recommended Skill: ahe-bug-patterns
