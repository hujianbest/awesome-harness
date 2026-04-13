# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T151
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: credential resolution and runtime home doctor diagnostics
- positive_cases:
  - resolver returns configured credential
  - doctor returns ok on valid layout
- negative_cases:
  - missing credential returns `missing_credential`
  - missing workspace returns warn report
