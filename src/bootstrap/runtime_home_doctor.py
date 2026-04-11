"""Runtime home configuration diagnostics shared by CLI and other entries (T181)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterable

from foundation import RuntimeHomeBinding

from .credential_resolution import CredentialResolutionError, resolve_credential_refs
from .profile_loader import RuntimeProfileResolutionError, load_runtime_profile


class DoctorSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    MIGRATION_NEEDED = "migration-needed"


@dataclass(slots=True, frozen=True)
class DoctorFinding:
    """Single diagnostic; stable for JSON and Web surfaces."""

    code: str
    severity: DoctorSeverity
    message: str
    path: str | None = None


def diagnose_runtime_home(
    runtime_home: Path | RuntimeHomeBinding,
    *,
    profile_id: str = "default",
    runtime_capabilities: tuple[str, ...] = (),
    provider_hints: dict[str, str] | None = None,
) -> tuple[tuple[DoctorFinding, ...], bool]:
    """
    Inspect runtime home layout, profile authority, and credential resolution.

    Returns (findings, ok) where ok is False if any finding has severity ERROR.
    """

    binding = runtime_home if isinstance(runtime_home, RuntimeHomeBinding) else RuntimeHomeBinding.from_root(runtime_home)
    findings: list[DoctorFinding] = []

    findings.extend(_check_expected_directories(binding))
    findings.extend(_check_runtime_home_version(binding))
    findings.extend(_check_providers_json(binding))
    if any(f.severity == DoctorSeverity.ERROR for f in findings):
        return (tuple(findings), False)

    profile_path = binding.profiles_root / f"{profile_id}.json"
    if not profile_path.is_file():
        findings.append(
            DoctorFinding(
                code="profile.missing",
                severity=DoctorSeverity.ERROR,
                message=f"Profile {profile_id!r} is missing at {profile_path}.",
                path=str(profile_path),
            )
        )
        return (tuple(findings), False)

    try:
        profile = load_runtime_profile(
            binding,
            profile_id=profile_id,
            runtime_capabilities=runtime_capabilities,
            provider_hints=provider_hints,
        )
    except RuntimeProfileResolutionError as exc:
        findings.append(
            DoctorFinding(
                code="profile.authority_invalid",
                severity=DoctorSeverity.ERROR,
                message=str(exc),
                path=str(profile_path),
            )
        )
        return (tuple(findings), False)

    if profile.adapter_id is not None:
        adapter_path = binding.adapters_root / f"{profile.adapter_id}.json"
        if not adapter_path.is_file():
            findings.append(
                DoctorFinding(
                    code="adapter.missing",
                    severity=DoctorSeverity.ERROR,
                    message=f"Adapter {profile.adapter_id!r} metadata is missing at {adapter_path}.",
                    path=str(adapter_path),
                )
            )

    if profile.credential_refs:
        try:
            resolve_credential_refs(profile.credential_refs, binding)
        except CredentialResolutionError as exc:
            findings.append(
                DoctorFinding(
                    code="credentials.unresolved",
                    severity=DoctorSeverity.ERROR,
                    message=str(exc),
                    path=str(binding.config_root),
                )
            )

    ok = not any(f.severity == DoctorSeverity.ERROR for f in findings)
    return (tuple(findings), ok)


def findings_as_jsonable(findings: Iterable[DoctorFinding]) -> list[dict[str, Any]]:
    return [
        {
            "code": f.code,
            "severity": f.severity.value,
            "message": f.message,
            **({"path": f.path} if f.path else {}),
        }
        for f in findings
    ]


def _check_expected_directories(binding: RuntimeHomeBinding) -> list[DoctorFinding]:
    out: list[DoctorFinding] = []
    for name, path in (
        ("profiles", binding.profiles_root),
        ("config", binding.config_root),
        ("adapters", binding.adapters_root),
        ("cache", binding.cache_root),
    ):
        if not path.is_dir():
            out.append(
                DoctorFinding(
                    code=f"layout.missing_{name}",
                    severity=DoctorSeverity.WARNING,
                    message=f"Expected runtime home directory {name!r} is missing; create {path} or migrate your layout.",
                    path=str(path),
                )
            )
    return out


def _check_providers_json(binding: RuntimeHomeBinding) -> list[DoctorFinding]:
    path = binding.config_root / "providers.json"
    if not path.is_file():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [
            DoctorFinding(
                code="config.providers_invalid",
                severity=DoctorSeverity.ERROR,
                message=f"providers.json is not valid JSON: {exc}",
                path=str(path),
            )
        ]
    if not isinstance(raw, dict):
        return [
            DoctorFinding(
                code="config.providers_shape",
                severity=DoctorSeverity.ERROR,
                message="providers.json must contain a JSON object at the top level.",
                path=str(path),
            )
        ]
    return []


def _check_runtime_home_version(binding: RuntimeHomeBinding) -> list[DoctorFinding]:
    """Safe migration hook: explicit version file under config/ (optional)."""

    marker = binding.config_root / "runtime-home-version"
    if not marker.is_file():
        return []
    text = marker.read_text(encoding="utf-8").strip()
    if text == "1":
        return []
    return [
        DoctorFinding(
            code="migration.version_mismatch",
            severity=DoctorSeverity.MIGRATION_NEEDED,
            message=(
                f"runtime-home-version is {text!r}; expected '1'. "
                "Review migration notes before relying on this runtime home."
            ),
            path=str(marker),
        )
    ]
