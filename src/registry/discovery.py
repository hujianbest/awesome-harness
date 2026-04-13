from __future__ import annotations

from contracts.validation import ContractValidationError, ContractValidator


class ContractRegistry:
    def __init__(self, validator: ContractValidator) -> None:
        self._validator = validator
        self._schemas: dict[str, dict[str, object]] = {}

    def register(self, schema: dict[str, object]) -> None:
        self._validator.validate(schema)
        self._schemas[str(schema["name"])] = dict(schema)

    def discover(self, name: str) -> dict[str, object]:
        schema = self._schemas.get(name)
        if schema is None:
            raise ContractValidationError("contract_missing", f"Contract '{name}' does not exist.")
        return dict(schema)
