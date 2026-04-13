# Test Design Approval Record

- approval_kind: 测试设计确认
- resolution_mode: auto
- task_id: T143
- based_on_task_plan: docs/tasks/2026-04-13-garage-mainline-tasks.md
- resolved_at: 2026-04-13
- next_action_or_recommended_skill: ahe-test-driven-dev

## Test Design Summary

- behavior: cross-pack handoff/rework/lineage workflow
- positive_cases:
  - accepted handoff emits lineage reference
- negative_cases:
  - rework without parent returns `parent_missing`
- fail_first_target:
  - missing `bridge.workflow` import path should fail before implementation
