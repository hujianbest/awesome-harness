from session.runtime import SessionRuntime, SessionStateError


def test_session_runtime_allows_active_to_interrupted_to_active():
    runtime = SessionRuntime()
    sid = runtime.create("default")
    runtime.transition(sid, "interrupt")
    runtime.transition(sid, "resume")
    state = runtime.get_state(sid)
    assert state == "active"


def test_session_runtime_rejects_invalid_transition():
    runtime = SessionRuntime()
    sid = runtime.create("default")
    try:
        runtime.transition(sid, "resume")
    except SessionStateError as exc:
        assert exc.code == "invalid_transition"
    else:
        raise AssertionError("expected invalid_transition")
