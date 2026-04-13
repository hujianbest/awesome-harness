from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContractValidationError(Exception):
    code: str
    message: str


class ContractValidator:
    def validate(self, schema: dict[str, object]) -> None:
        required = {"name", "version", "fields"}
        if not required.issubset(schema.keys()):
            raise ContractValidationError("invalid_schema", "Schema is missing required keys.")
        if not isinstance(schema["fields"], list) or not schema["fields"]:
            raise ContractValidationError("invalid_schema", "Schema fields must be a non-empty list.")
