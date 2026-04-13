from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PackError(Exception):
    code: str
    message: str


class PackCatalog:
    def __init__(self) -> None:
        self._packs: dict[str, dict[str, str]] = {}

    def register(self, metadata: dict[str, str]) -> None:
        required = {"id", "kind", "version"}
        if not required.issubset(metadata.keys()):
            raise PackError("invalid_pack_metadata", "Pack metadata is missing required keys.")
        self._packs[metadata["id"]] = dict(metadata)

    def get(self, pack_id: str) -> dict[str, str]:
        pack = self._packs.get(pack_id)
        if pack is None:
            raise PackError("pack_missing", f"Pack '{pack_id}' does not exist.")
        return dict(pack)
