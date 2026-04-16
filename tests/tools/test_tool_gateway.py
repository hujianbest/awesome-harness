"""Tests for tool_gateway module."""

import pytest

from garage_os.tools.tool_gateway import ToolGateway


@pytest.fixture
def open_gateway() -> ToolGateway:
    """Gateway with no whitelist (open mode)."""
    return ToolGateway()


@pytest.fixture
def restricted_gateway() -> ToolGateway:
    """Gateway with a whitelist."""
    return ToolGateway(whitelist=["allowed_tool", "another_ok"])


class TestPermissionCheck:
    """White-list based permission checks."""

    def test_open_mode_allows_everything(self, open_gateway: ToolGateway) -> None:
        assert open_gateway.check_permission("any_tool") is True

    def test_whitelist_allows_listed(self, restricted_gateway: ToolGateway) -> None:
        assert restricted_gateway.check_permission("allowed_tool") is True

    def test_whitelist_rejects_unlisted(self, restricted_gateway: ToolGateway) -> None:
        assert restricted_gateway.check_permission("forbidden") is False

    def test_empty_whitelist_is_open(self) -> None:
        gw = ToolGateway(whitelist=[])
        assert gw.check_permission("anything") is True


class TestCallTool:
    """call_tool behaviour and call logging."""

    def test_call_allowed_tool(self, restricted_gateway: ToolGateway) -> None:
        result = restricted_gateway.call_tool("allowed_tool", {"q": "hello"})
        assert result["status"] == "ok"
        assert result["tool_id"] == "allowed_tool"
        assert "call_id" in result
        assert result["result"]["mock"] is True
        assert result["result"]["echo_args"] == {"q": "hello"}

    def test_call_denied_tool(self, restricted_gateway: ToolGateway) -> None:
        result = restricted_gateway.call_tool("blocked_tool")
        assert result["status"] == "denied"
        assert result["error"] == "permission_denied"

    def test_call_open_gateway(self, open_gateway: ToolGateway) -> None:
        result = open_gateway.call_tool("whatever")
        assert result["status"] == "ok"


class TestCallLog:
    """Call log entries contain tool_id, duration, and result."""

    def test_log_records_tool_id(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("tool_alpha")
        open_gateway.call_tool("tool_beta")

        log = open_gateway.get_call_log()
        assert len(log) == 2
        assert log[0]["tool_id"] == "tool_alpha"
        assert log[1]["tool_id"] == "tool_beta"

    def test_log_records_duration(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("timed_tool")
        log = open_gateway.get_call_log()
        assert len(log) == 1
        assert isinstance(log[0]["duration_ms"], float)
        assert log[0]["duration_ms"] >= 0

    def test_log_records_result(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("res_tool", {"x": 1})
        log = open_gateway.get_call_log()
        assert log[0]["result"]["mock"] is True
        assert log[0]["result"]["echo_args"] == {"x": 1}

    def test_log_records_denied(self, restricted_gateway: ToolGateway) -> None:
        restricted_gateway.call_tool("denied_one")
        log = restricted_gateway.get_call_log()
        assert len(log) == 1
        assert log[0]["allowed"] is False
        assert log[0]["error"] == "permission_denied"

    def test_get_call_log_filter_by_tool(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("aaa")
        open_gateway.call_tool("bbb")
        open_gateway.call_tool("aaa")

        aaa_log = open_gateway.get_call_log(tool_id="aaa")
        assert len(aaa_log) == 2
        assert all(e["tool_id"] == "aaa" for e in aaa_log)

    def test_call_id_unique(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("t")
        open_gateway.call_tool("t")
        log = open_gateway.get_call_log()
        ids = {e["call_id"] for e in log}
        assert len(ids) == 2


class TestPhase1Mock:
    """Phase 1: call_tool returns mock results; real execution by Skill Executor."""

    def test_mock_result_structure(self, open_gateway: ToolGateway) -> None:
        result = open_gateway.call_tool("mock_check")
        assert result["status"] == "ok"
        assert result["result"]["mock"] is True
        assert "Skill Executor" in result["result"]["message"]

    def test_timestamp_present(self, open_gateway: ToolGateway) -> None:
        open_gateway.call_tool("ts_tool")
        log = open_gateway.get_call_log()
        assert log[0]["timestamp"]  # non-empty ISO string
