from execution.runtime import ExecutionRuntime, ExecutionError


def test_execution_runtime_accepts_safe_tool_action():
    runtime = ExecutionRuntime()
    result = runtime.execute(
        session_id="sess-1", action={"tool": "echo", "input": "hello"}, authority="runtime"
    )
    assert result["status"] == "accepted"
    assert result["trace_ref"].startswith("trace:")


def test_execution_runtime_rejects_authority_override():
    runtime = ExecutionRuntime()
    try:
        runtime.execute(
            session_id="sess-1",
            action={"tool": "override_provider"},
            authority="host",
        )
    except ExecutionError as exc:
        assert exc.code == "authority_violation"
    else:
        raise AssertionError("expected authority_violation")
