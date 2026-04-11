"""Concrete HostBridgeEntry adapter guards (T210+).

Callers in host shells validate the launch request before invoking
HostBridgeSessionApi so the correct catalog binding is always used.
"""

from __future__ import annotations

from .host_bridge import HostBridgeLaunchRequest
from .launcher import BootstrapError

CURSOR_HOST_ADAPTER_ID = "cursor"


def require_cursor_host_bridge(request: HostBridgeLaunchRequest) -> HostBridgeLaunchRequest:
    if request.host_adapter_id != CURSOR_HOST_ADAPTER_ID:
        raise GarageHostAdapterError(
            f"Cursor host bridge requires host_adapter_id {CURSOR_HOST_ADAPTER_ID!r}, "
            f"got {request.host_adapter_id!r}."
        )
    return request


class GarageHostAdapterError(BootstrapError):
    """Raised when a concrete host shell misconfigures the bridge request."""

