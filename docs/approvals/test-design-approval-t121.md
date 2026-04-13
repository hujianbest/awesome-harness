# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T121
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: filebacked workspace facts/artifact routing
- positive_cases:
  - facts artifact routes into workspace facts path
- negative_cases:
  - unknown artifact kind returns `unknown_artifact_kind`
- fail_first_target:
  - missing `surfaces.filebacked` import path should fail before implementation
