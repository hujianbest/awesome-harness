"""Unified runtime launcher and bootstrap scaffolding."""

from redaction import redact_text

from .credential_resolution import (
    CredentialResolutionError,
    ResolvedCredentials,
    merge_credential_ref_declarations,
    resolve_credential_refs,
)
from .install_layout import (
    RUNTIME_HOME_SCHEMA_VERSION,
    default_runtime_home_path,
    package_version,
    resolve_runtime_home,
    resolve_source_root,
    resolve_workspace_root,
)
from .concrete_host_bridge import (
    CLAUDE_HOST_ADAPTER_ID,
    CURSOR_HOST_ADAPTER_ID,
    GarageHostAdapterError,
    require_claude_host_bridge,
    require_cursor_host_bridge,
)
from .host_bridge import HostBridgeLaunchRequest, HostBridgeSessionApi
from .runtime_home_doctor import DoctorFinding, DoctorSeverity, diagnose_runtime_home, findings_as_jsonable
from .runtime_ops import (
    HealthStatus,
    compute_install_diagnostics,
    launch_summary_diagnostics,
    ops_emit,
    recent_ops_events,
)
from .launcher import (
    BootstrapConfig,
    BootstrapError,
    GarageLauncher,
    LaunchMode,
    LaunchResult,
    RuntimeServices,
)
from .profile_loader import RuntimeProfileResolutionError, load_runtime_profile
from .session_api import SessionApi, SessionLaunchSummary
from .trace_ops import summarize_execution_trace
from .web import WebControlPlane, WebControlPlaneConfig, WebControlPlaneState

__all__ = [
    "BootstrapConfig",
    "BootstrapError",
    "CredentialResolutionError",
    "CLAUDE_HOST_ADAPTER_ID",
    "CURSOR_HOST_ADAPTER_ID",
    "DoctorFinding",
    "DoctorSeverity",
    "GarageHostAdapterError",
    "GarageLauncher",
    "HealthStatus",
    "RUNTIME_HOME_SCHEMA_VERSION",
    "HostBridgeLaunchRequest",
    "HostBridgeSessionApi",
    "LaunchMode",
    "LaunchResult",
    "ResolvedCredentials",
    "default_runtime_home_path",
    "RuntimeServices",
    "RuntimeProfileResolutionError",
    "SessionApi",
    "SessionLaunchSummary",
    "summarize_execution_trace",
    "WebControlPlane",
    "WebControlPlaneConfig",
    "WebControlPlaneState",
    "compute_install_diagnostics",
    "diagnose_runtime_home",
    "findings_as_jsonable",
    "launch_summary_diagnostics",
    "load_runtime_profile",
    "ops_emit",
    "package_version",
    "recent_ops_events",
    "merge_credential_ref_declarations",
    "redact_text",
    "resolve_credential_refs",
    "resolve_runtime_home",
    "resolve_source_root",
    "resolve_workspace_root",
    "require_claude_host_bridge",
    "require_cursor_host_bridge",
]
