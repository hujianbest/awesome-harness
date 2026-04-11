"""Unified runtime launcher and bootstrap scaffolding."""

from redaction import redact_text

from .credential_resolution import (
    CredentialResolutionError,
    ResolvedCredentials,
    merge_credential_ref_declarations,
    resolve_credential_refs,
)
from .host_bridge import HostBridgeLaunchRequest, HostBridgeSessionApi
from .runtime_home_doctor import DoctorFinding, DoctorSeverity, diagnose_runtime_home, findings_as_jsonable
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
from .web import WebControlPlane, WebControlPlaneConfig, WebControlPlaneState

__all__ = [
    "BootstrapConfig",
    "BootstrapError",
    "CredentialResolutionError",
    "DoctorFinding",
    "DoctorSeverity",
    "GarageLauncher",
    "HostBridgeLaunchRequest",
    "HostBridgeSessionApi",
    "LaunchMode",
    "LaunchResult",
    "ResolvedCredentials",
    "RuntimeServices",
    "RuntimeProfileResolutionError",
    "SessionApi",
    "SessionLaunchSummary",
    "WebControlPlane",
    "WebControlPlaneConfig",
    "WebControlPlaneState",
    "diagnose_runtime_home",
    "findings_as_jsonable",
    "load_runtime_profile",
    "merge_credential_ref_declarations",
    "redact_text",
    "resolve_credential_refs",
]
