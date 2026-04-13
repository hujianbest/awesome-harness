from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ContinuityError(Exception):
    code: str
    message: str


class ContinuityStore:
    def __init__(self) -> None:
        self._buckets: dict[str, dict[str, Any]] = {"memory": {}, "skills": {}}

    def write(self, bucket: str, key: str, value: Any) -> None:
        store = self._buckets.get(bucket)
        if store is None:
            raise ContinuityError("unknown_bucket", f"Unknown continuity bucket: {bucket}")
        store[key] = value

    def read(self, bucket: str, key: str) -> Any:
        store = self._buckets.get(bucket)
        if store is None:
            raise ContinuityError("unknown_bucket", f"Unknown continuity bucket: {bucket}")
        return store[key]
