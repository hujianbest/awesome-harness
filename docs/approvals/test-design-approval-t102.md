# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T102
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: Web control plane create/resume and workspace facts fallback
- positive_cases:
  - create then resume preserves active session identity
- negative_cases:
  - workspace facts unavailable fallback returns stale snapshot flag
- fail_first_target:
  - missing `bootstrap.web` import path should fail before implementation
