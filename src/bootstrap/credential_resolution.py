"""Shared secrets / credential reference resolution for runtime home (T180)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from foundation import RuntimeHomeBinding
from redaction import redact_text


class CredentialResolutionError(RuntimeError):
    """Raised when a credential reference cannot be resolved safely."""


@dataclass(slots=True, frozen=True)
class ResolvedCredentials:
    """Resolved secret material for execution; treat as sensitive."""

    values: Mapping[str, str]

    def as_safe_metadata(self) -> dict[str, str]:
        """Metadata safe for logs and traces (values redacted)."""
        return {key: "[REDACTED]" for key in self.values}


_SECRETISH_KEY = re.compile(
    r"(?i)(secret|token|password|apikey|api_key|credential|bearer|auth)",
)


def merge_credential_ref_declarations(
    profile_mapping: Mapping[str, Any],
    profile_overrides: Mapping[str, Any],
    defaults: Mapping[str, Any],
    adapter_mapping: Mapping[str, Any],
) -> dict[str, str]:
    """Merge credential slot -> reference string; later layers override earlier (profile wins last)."""

    merged: dict[str, str] = {}
    for layer in (adapter_mapping, defaults, profile_overrides, profile_mapping):
        layer_refs = _extract_refs_from_layer(layer)
        merged.update(layer_refs)
    return merged


def resolve_credential_refs(
    refs: Mapping[str, str],
    runtime_home: RuntimeHomeBinding,
) -> ResolvedCredentials:
    values: dict[str, str] = {}
    for slot, ref in refs.items():
        values[slot] = _resolve_single_ref(ref.strip(), runtime_home, slot=slot)
    return ResolvedCredentials(values=values)


def _extract_refs_from_layer(layer: Mapping[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    credentials = layer.get("credentials")
    if isinstance(credentials, dict):
        for raw_key, raw_val in credentials.items():
            if not isinstance(raw_key, str) or not raw_key.strip():
                raise CredentialResolutionError("Credential slot names must be non-empty strings.")
            if not isinstance(raw_val, str) or not raw_val.strip():
                raise CredentialResolutionError(f"Credential reference for slot {raw_key!r} must be a non-empty string.")
            slot = raw_key.strip()
            out[slot] = raw_val.strip()

    ref_keys: dict[str, str] = {}
    for key, val in layer.items():
        if key == "credentials":
            continue
        if isinstance(key, str) and key.endswith("Ref") and isinstance(val, str) and val.strip():
            slot = key[:-3]
            if not slot:
                raise CredentialResolutionError(f"Invalid credential reference key {key!r}.")
            ref_keys[slot] = val.strip()

    for slot, ref in ref_keys.items():
        if slot in out and out[slot] != ref:
            raise CredentialResolutionError(
                f"Conflicting credential references for slot {slot!r} in the same configuration layer."
            )
        if slot not in out:
            out[slot] = ref

    return out


def _resolve_single_ref(ref: str, runtime_home: RuntimeHomeBinding, *, slot: str) -> str:
    if ":" not in ref:
        raise CredentialResolutionError(
            f"Credential slot {slot!r}: reference {ref!r} must use a scheme prefix (env: or runtime-config:)."
        )
    scheme, _, rest = ref.partition(":")
    rest = rest.strip()
    if not rest:
        raise CredentialResolutionError(f"Credential slot {slot!r}: empty reference body for scheme {scheme!r}.")

    if scheme == "env":
        value = os.environ.get(rest)
        if value is None or not value.strip():
            raise CredentialResolutionError(
                f"Credential slot {slot!r}: environment variable {rest!r} is missing or empty."
            )
        return value.strip()

    if scheme == "runtime-config":
        return _read_runtime_config_file(rest, runtime_home, slot=slot)

    raise CredentialResolutionError(
        f"Credential slot {slot!r}: unsupported reference scheme {scheme!r} (expected env or runtime-config)."
    )


def _read_runtime_config_file(rel_path: str, runtime_home: RuntimeHomeBinding, *, slot: str) -> str:
    candidate = Path(rel_path)
    if candidate.is_absolute():
        raise CredentialResolutionError(
            f"Credential slot {slot!r}: runtime-config path must be relative, got {rel_path!r}."
        )
    if ".." in candidate.parts:
        raise CredentialResolutionError(
            f"Credential slot {slot!r}: path {rel_path!r} must not contain parent segments."
        )
    resolved = (runtime_home.config_root / candidate).resolve()
    try:
        resolved.relative_to(runtime_home.config_root.resolve())
    except ValueError as exc:
        raise CredentialResolutionError(
            f"Credential slot {slot!r}: path {rel_path!r} escapes runtime config_root."
        ) from exc
    if not resolved.is_file():
        raise CredentialResolutionError(
            f"Credential slot {slot!r}: runtime-config file {resolved} does not exist or is not a file."
        )
    text = resolved.read_text(encoding="utf-8").strip()
    if not text:
        raise CredentialResolutionError(f"Credential slot {slot!r}: file {resolved} is empty.")
    return text


def metadata_str(metadata: Mapping[str, str], *, known_secrets: Mapping[str, str] | None = None) -> dict[str, str]:
    """Copy metadata with redaction applied to values that look sensitive or match known secrets."""

    out: dict[str, str] = {}
    for key, val in metadata.items():
        if _SECRETISH_KEY.search(key):
            out[key] = "[REDACTED]"
            continue
        out[key] = redact_text(val, known_values=known_secrets)
    return out
