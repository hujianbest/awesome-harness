import json
import tempfile
import unittest
import urllib.request
from pathlib import Path

from bootstrap import (
    BootstrapConfig,
    LaunchMode,
    SessionApi,
    WebControlPlane,
)
from session import SessionAction
from session.lifecycle import apply_action


class WebControlPlaneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_web_control_plane_reports_health(self) -> None:
        control_plane = WebControlPlane()
        state = control_plane.start()
        try:
            with urllib.request.urlopen(f"{state.base_url}/health") as response:
                payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(payload["status"], "healthy")
            self.assertEqual(payload["entrySurface"], "web")
            self.assertEqual(payload["hostAdapterId"], "web")
        finally:
            control_plane.stop()

    def test_web_control_plane_creates_and_resumes_sessions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_home = Path(tmp_dir) / "runtime-home"
            workspace_root = Path(tmp_dir) / "workspace"
            control_plane = WebControlPlane()
            state = control_plane.start()
            try:
                created = self._post_json(
                    f"{state.base_url}/sessions/create",
                    {
                        "sourceRoot": str(self.repo_root),
                        "runtimeHome": str(runtime_home),
                        "workspaceRoot": str(workspace_root),
                        "workspaceId": "garage-workspace",
                        "profileId": "dogfood",
                        "problemKind": "implementation",
                        "entryPack": "coding",
                        "entryNode": "coding.bridge-intake",
                        "goal": "Land the web entry slice.",
                    },
                )
                self.assertEqual(created["hostAdapterId"], "web")

                session_id = created["sessionId"]
                paused = SessionApi().create(
                    BootstrapConfig(
                        launch_mode=LaunchMode.CREATE,
                        source_root=self.repo_root,
                        runtime_home=runtime_home,
                        workspace_root=workspace_root,
                        workspace_id="garage-workspace",
                        profile_id="dogfood",
                        entry_surface="cli",
                        problem_kind="implementation",
                        entry_pack="coding",
                        entry_node="coding.bridge-intake",
                        goal="Pause for web resume coverage.",
                    )
                )
                paused_state = apply_action(
                    paused.session_state,
                    SessionAction.PAUSE,
                    summary="Paused before resuming through WebEntry.",
                )
                paused.services.surfaces.write_session_state(paused_state)

                resumed = self._post_json(
                    f"{state.base_url}/sessions/resume",
                    {
                        "sourceRoot": str(self.repo_root),
                        "runtimeHome": str(runtime_home),
                        "workspaceRoot": str(workspace_root),
                        "workspaceId": "garage-workspace",
                        "profileId": "dogfood",
                        "sessionId": paused_state.session_id,
                    },
                )
                self.assertEqual(resumed["hostAdapterId"], "web")
                self.assertEqual(resumed["sessionId"], paused_state.session_id)
                self.assertNotEqual(session_id, "")
            finally:
                control_plane.stop()

    @staticmethod
    def _post_json(url: str, payload: dict[str, str]) -> dict[str, str]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
