from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CredentialError(Exception):
    code: str
    message: str


class CredentialResolver:
    def __init__(self, env: dict[str, str]) -> None:
        self._env = env

    def resolve(self, key: str) -> str:
        value = self._env.get(key)
        if value is None:
            raise CredentialError("missing_credential", f"Credential '{key}' is not configured.")
        return value
