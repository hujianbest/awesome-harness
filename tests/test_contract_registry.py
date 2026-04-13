from contracts.validation import ContractValidator, ContractValidationError
from registry.discovery import ContractRegistry


def test_contract_registry_register_and_discover_contract():
    validator = ContractValidator()
    registry = ContractRegistry(validator)
    schema = {"name": "session.contract", "version": "1.0", "fields": ["session_id", "status"]}
    registry.register(schema)
    loaded = registry.discover("session.contract")
    assert loaded["version"] == "1.0"


def test_contract_registry_rejects_invalid_schema():
    validator = ContractValidator()
    registry = ContractRegistry(validator)
    try:
        registry.register({"name": "bad.contract"})
    except ContractValidationError as exc:
        assert exc.code == "invalid_schema"
    else:
        raise AssertionError("expected invalid_schema")
