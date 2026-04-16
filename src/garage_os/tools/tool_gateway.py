"""Tool Gateway — permission checks, call logging, and Phase-1 mock invocation."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CallLogEntry:
    """A single tool-call log record."""

    call_id: str
    tool_id: str
    arguments: Dict[str, Any]
    allowed: bool
    result: Optional[Any]
    duration_ms: float
    timestamp: str
    error: Optional[str] = None


class ToolGateway:
    """Mediates tool access: permission checks + call logging.

    Phase-1 simplification
    ----------------------
    ``call_tool`` does **not** actually execute any tool.  It records the call
    in an in-memory log and returns a mock result dict.  Real execution will
    be handled by the *Skill Executor* through the *Host Adapter* in a later
    phase.
    """

    def __init__(
        self,
        *,
        whitelist: Optional[List[str]] = None,
    ) -> None:
        """Initialise the gateway.

        Args:
            whitelist: List of tool_ids that are permitted.  If *None* or
                       empty, **all** tools are allowed (open mode).
        """
        # Normalise to a set for O(1) lookups; empty set ⇒ open mode.
        self._whitelist: set[str] = set(whitelist) if whitelist else set()
        self._call_log: List[CallLogEntry] = []

    # ------------------------------------------------------------------
    # Permission
    # ------------------------------------------------------------------

    def check_permission(self, tool_id: str) -> bool:
        """Check whether *tool_id* is permitted.

        When no whitelist was supplied (or it is empty), every tool is
        allowed.  Otherwise the tool must appear in the whitelist.

        Args:
            tool_id: Identifier of the tool to check.

        Returns:
            ``True`` if the call is allowed, ``False`` otherwise.
        """
        # Open mode: everything allowed
        if not self._whitelist:
            return True
        return tool_id in self._whitelist

    # ------------------------------------------------------------------
    # Call (Phase 1: mock)
    # ------------------------------------------------------------------

    def call_tool(
        self,
        tool_id: str,
        arguments: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Invoke a tool (Phase 1: mock) and record the call.

        The method performs a permission check first.  If the tool is not
        whitelisted the call is still logged (with ``allowed=False``) and a
        rejection dict is returned.

        Args:
            tool_id:   Identifier of the tool to call.
            arguments: Keyword arguments forwarded to the tool.

        Returns:
            A result dict containing at minimum ``"status"``, ``"tool_id"``,
            and ``"call_id"``.
        """
        call_id = _new_call_id()
        args = arguments or {}
        start = time.monotonic()

        allowed = self.check_permission(tool_id)

        if not allowed:
            duration_ms = (time.monotonic() - start) * 1000
            entry = CallLogEntry(
                call_id=call_id,
                tool_id=tool_id,
                arguments=args,
                allowed=False,
                result=None,
                duration_ms=duration_ms,
                timestamp=datetime.now().isoformat(),
                error="permission_denied",
            )
            self._call_log.append(entry)
            return {
                "status": "denied",
                "tool_id": tool_id,
                "call_id": call_id,
                "error": "permission_denied",
            }

        # Phase 1: mock execution
        mock_result = {
            "mock": True,
            "tool_id": tool_id,
            "echo_args": args,
            "message": "Phase 1 mock — real execution by Skill Executor",
        }

        duration_ms = (time.monotonic() - start) * 1000
        entry = CallLogEntry(
            call_id=call_id,
            tool_id=tool_id,
            arguments=args,
            allowed=True,
            result=mock_result,
            duration_ms=duration_ms,
            timestamp=datetime.now().isoformat(),
        )
        self._call_log.append(entry)

        return {
            "status": "ok",
            "tool_id": tool_id,
            "call_id": call_id,
            "result": mock_result,
            "duration_ms": duration_ms,
        }

    # ------------------------------------------------------------------
    # Call log
    # ------------------------------------------------------------------

    def get_call_log(self, tool_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return call log entries.

        Args:
            tool_id: If given, filter entries to this tool.

        Returns:
            List of log-entry dicts.
        """
        entries = self._call_log
        if tool_id is not None:
            entries = [e for e in entries if e.tool_id == tool_id]

        return [
            {
                "call_id": e.call_id,
                "tool_id": e.tool_id,
                "arguments": e.arguments,
                "allowed": e.allowed,
                "result": e.result,
                "duration_ms": e.duration_ms,
                "timestamp": e.timestamp,
                "error": e.error,
            }
            for e in entries
        ]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _new_call_id() -> str:
    """Generate a unique call identifier."""
    return f"call-{uuid.uuid4().hex[:12]}"
