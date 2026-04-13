# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T111
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: runtime home/workspace topology binding and profile authority checks
- positive_cases:
  - bind workspace returns topology including runtime_home and workspace_path
- negative_cases:
  - unsupported profile returns `profile_denied`
- fail_first_target:
  - missing `bootstrap.runtime_home` should fail before implementation
