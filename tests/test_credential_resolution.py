from bootstrap.credential_resolution import CredentialResolver, CredentialError


def test_credential_resolver_returns_runtime_scoped_secret():
    resolver = CredentialResolver({"OPENAI_API_KEY": "sk-test"})
    secret = resolver.resolve("OPENAI_API_KEY")
    assert secret == "sk-test"


def test_credential_resolver_raises_for_missing_secret():
    resolver = CredentialResolver({})
    try:
        resolver.resolve("OPENAI_API_KEY")
    except CredentialError as exc:
        assert exc.code == "missing_credential"
    else:
        raise AssertionError("expected missing_credential")
