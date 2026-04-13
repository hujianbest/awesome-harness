# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T101
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: CLI create/resume/attach/step minimal path through shared SessionApi
- positive_cases:
  - create then resume returns same session identity
- negative_cases:
  - attach with unknown workspace returns `workspace_not_found`
  - step on missing session returns `session_missing`
- fail_first_target:
  - missing `bootstrap.cli` / `SessionApi` import path should fail before implementation

## Notes

- Approval auto-resolved under `Execution Mode=auto`.
