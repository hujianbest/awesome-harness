from execution.runtime import ExecutionRuntime


def test_execution_runtime_generates_trace_and_evidence_refs():
    runtime = ExecutionRuntime()
    result = runtime.execute(
        session_id="sess-1", action={"tool": "echo", "input": "ping"}, authority="runtime"
    )
    assert result["trace_ref"].startswith("trace:")
    assert result["evidence_ref"].startswith("evidence:")
