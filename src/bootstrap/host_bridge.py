"""Thin host-bridge entry helpers that reuse SessionApi and shared bootstrap."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from .launcher import BootstrapConfig, BootstrapError, LaunchMode, LaunchResult
from .session_api import SessionApi


@dataclass(slots=True, frozen=True)
class HostBridgeLaunchRequest:
    host_adapter_id: str
    launch_mode: LaunchMode
    source_root: Path
    runtime_home: Path
    workspace_root: Path
    workspace_id: str | None = None
    profile_id: str = "default"
    session_id: str | None = None
    initiator: str = "creator"
    problem_kind: str | None = None
    entry_pack: str | None = None
    entry_node: str | None = None
    goal: str | None = None
    summary: str | None = None
    boundaries: tuple[str, ...] = ()
    runtime_capabilities: tuple[str, ...] = ()
    provider_hints: Mapping[str, str] = field(default_factory=dict)


class HostBridgeSessionApi:
    """Map host-specific launch requests onto the shared SessionApi seam."""

    def __init__(self, session_api: SessionApi | None = None) -> None:
        self._session_api = session_api or SessionApi()

    def launch(self, request: HostBridgeLaunchRequest, *, existing_state=None) -> LaunchResult:
        result = self._session_api.launch(
            BootstrapConfig(
                launch_mode=request.launch_mode,
                source_root=request.source_root,
                runtime_home=request.runtime_home,
                workspace_root=request.workspace_root,
                workspace_id=request.workspace_id,
                profile_id=request.profile_id,
                entry_surface="host-bridge",
                host_adapter_id=request.host_adapter_id,
                session_id=request.session_id,
                initiator=request.initiator,
                problem_kind=request.problem_kind,
                entry_pack=request.entry_pack,
                entry_node=request.entry_node,
                goal=request.goal,
                summary=request.summary,
                boundaries=request.boundaries,
                runtime_capabilities=request.runtime_capabilities,
                provider_hints=request.provider_hints,
            ),
            existing_state=existing_state,
        )
        if result.services.host.host_kind != "host-bridge":
            raise BootstrapError(
                f"Host adapter {result.services.host.adapter_id!r} is not bound as a HostBridgeEntry."
            )
        return result

    def create(self, request: HostBridgeLaunchRequest, *, existing_state=None) -> LaunchResult:
        self._require_mode(request, LaunchMode.CREATE)
        return self.launch(request, existing_state=existing_state)

    def resume(self, request: HostBridgeLaunchRequest, *, existing_state=None) -> LaunchResult:
        self._require_mode(request, LaunchMode.RESUME)
        return self.launch(request, existing_state=existing_state)

    def attach(self, request: HostBridgeLaunchRequest, *, existing_state=None) -> LaunchResult:
        self._require_mode(request, LaunchMode.ATTACH)
        return self.launch(request, existing_state=existing_state)

    @staticmethod
    def _require_mode(request: HostBridgeLaunchRequest, expected: LaunchMode) -> None:
        if request.launch_mode != expected:
            raise ValueError(
                f"HostBridgeSessionApi expected launch mode {expected.value!r}, got {request.launch_mode.value!r}."
            )
