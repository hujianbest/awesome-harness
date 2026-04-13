from bootstrap.runtime_home import RuntimeHome


def test_install_layout_reports_runtime_home_and_workspace():
    home = RuntimeHome(root="D:/Garage/.garage")
    topology = home.bind_workspace("default", profile="dev")
    assert topology["runtime_home"] == "D:/Garage/.garage"
    assert topology["workspace_path"].endswith("/workspaces/default")
