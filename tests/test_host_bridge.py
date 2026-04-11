import tempfile
import unittest
from pathlib import Path

from bootstrap import (
    BootstrapError,
    HostBridgeLaunchRequest,
    HostBridgeSessionApi,
    LaunchMode,
)
from core import SessionStatus
from session import SessionAction
from session.lifecycle import apply_action


class HostBridgeSessionApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.host_bridge = HostBridgeSessionApi()

    def test_host_bridge_create_uses_host_bridge_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir) / "workspace"
            runtime_home = Path(tmp_dir) / "runtime-home"
            result = self.host_bridge.create(
                HostBridgeLaunchRequest(
                    host_adapter_id="cursor",
                    launch_mode=LaunchMode.CREATE,
                    source_root=self.repo_root,
                    runtime_home=runtime_home,
                    workspace_root=workspace_root,
                    workspace_id="garage-workspace",
                    profile_id="dogfood",
                    problem_kind="implementation",
                    entry_pack="coding",
                    entry_node="coding.bridge-intake",
                    goal="Land the host bridge slice.",
                )
            )

            self.assertEqual(result.services.host.adapter_id, "cursor")
            self.assertEqual(result.services.host.host_kind, "host-bridge")
            self.assertEqual(result.session_state.session_status, SessionStatus.ACTIVE)

    def test_host_bridge_resume_allows_switching_bridge_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir) / "workspace"
            runtime_home = Path(tmp_dir) / "runtime-home"
            created = self.host_bridge.create(
                HostBridgeLaunchRequest(
                    host_adapter_id="cursor",
                    launch_mode=LaunchMode.CREATE,
                    source_root=self.repo_root,
                    runtime_home=runtime_home,
                    workspace_root=workspace_root,
                    workspace_id="garage-workspace",
                    profile_id="dogfood",
                    problem_kind="implementation",
                    entry_pack="coding",
                    entry_node="coding.bridge-intake",
                    goal="Land the host bridge slice.",
                )
            )
            paused_state = apply_action(
                created.session_state,
                SessionAction.PAUSE,
                summary="Paused while switching host bridge adapters.",
            )
            created.services.surfaces.write_session_state(paused_state)

            resumed = self.host_bridge.resume(
                HostBridgeLaunchRequest(
                    host_adapter_id="claude",
                    launch_mode=LaunchMode.RESUME,
                    source_root=self.repo_root,
                    runtime_home=runtime_home,
                    workspace_root=workspace_root,
                    workspace_id="garage-workspace",
                    profile_id="dogfood",
                    session_id=paused_state.session_id,
                )
            )

            self.assertEqual(resumed.services.host.adapter_id, "claude")
            self.assertEqual(resumed.services.host.host_kind, "host-bridge")
            self.assertEqual(resumed.session_state.session_status, SessionStatus.ACTIVE)

    def test_host_bridge_rejects_non_bridge_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir) / "workspace"
            runtime_home = Path(tmp_dir) / "runtime-home"
            with self.assertRaises(BootstrapError):
                self.host_bridge.create(
                    HostBridgeLaunchRequest(
                        host_adapter_id="cli",
                        launch_mode=LaunchMode.CREATE,
                        source_root=self.repo_root,
                        runtime_home=runtime_home,
                        workspace_root=workspace_root,
                        workspace_id="garage-workspace",
                        profile_id="dogfood",
                        problem_kind="implementation",
                        entry_pack="coding",
                        entry_node="coding.bridge-intake",
                        goal="This should stay outside the host bridge seam.",
                    )
                )


if __name__ == "__main__":
    unittest.main()
