import io
import json

from bootstrap.cli import execute
from bootstrap.session_api import SessionApi


def run_cli(argv, api):
    out = io.StringIO()
    err = io.StringIO()
    code = execute(argv, api=api, out=out, err=err)
    return code, out.getvalue().strip(), err.getvalue().strip()


def test_create_and_resume_session_roundtrip():
    api = SessionApi()

    code, out, err = run_cli(
        ["create", "--team", "garage", "--workspace", "default", "--profile", "dev"], api
    )
    assert code == 0, err
    payload = json.loads(out)
    assert payload["status"] == "active"
    session_id = payload["session_id"]

    code, out, err = run_cli(["resume", "--session", session_id], api)
    assert code == 0, err
    payload = json.loads(out)
    assert payload["session_id"] == session_id
    assert payload["status"] == "active"


def test_attach_reports_unified_error_for_missing_workspace():
    api = SessionApi()
    code, out, err = run_cli(
        ["create", "--team", "garage", "--workspace", "default", "--profile", "dev"], api
    )
    assert code == 0, err
    session_id = json.loads(out)["session_id"]

    code, _, err = run_cli(["attach", "--session", session_id, "--workspace", "unknown"], api)
    assert code == 1
    payload = json.loads(err)
    assert payload["error"] == "workspace_not_found"


def test_step_reports_missing_session_error():
    api = SessionApi()

    code, _, err = run_cli(["step", "--session", "missing", "--input", "hello"], api)
    assert code == 1
    payload = json.loads(err)
    assert payload["error"] == "session_missing"
