from bootstrap.runtime_home import RuntimeHome, RuntimeHomeError


def test_runtime_home_bind_workspace_success():
    home = RuntimeHome(root="D:/Garage/.garage")
    topology = home.bind_workspace("default", profile="dev")
    assert topology["workspace_id"] == "default"
    assert topology["profile"] == "dev"
    assert topology["runtime_home"].endswith(".garage")


def test_runtime_home_rejects_unknown_profile():
    home = RuntimeHome(root="D:/Garage/.garage")
    try:
        home.bind_workspace("default", profile="unknown")
    except RuntimeHomeError as exc:
        assert exc.code == "profile_denied"
    else:
        raise AssertionError("expected profile_denied")
