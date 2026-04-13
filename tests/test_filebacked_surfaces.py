from surfaces.filebacked import FilebackedSurface, SurfaceRoutingError


def test_filebacked_surface_routes_artifact_to_workspace_facts():
    surface = FilebackedSurface(root="D:/Garage/.garage")
    result = surface.route_artifact("default", "facts", "session.json")
    assert result.endswith("/workspaces/default/facts/session.json")


def test_filebacked_surface_rejects_unknown_artifact_kind():
    surface = FilebackedSurface(root="D:/Garage/.garage")
    try:
        surface.route_artifact("default", "unknown", "x.json")
    except SurfaceRoutingError as exc:
        assert exc.code == "unknown_artifact_kind"
    else:
        raise AssertionError("expected unknown_artifact_kind")
