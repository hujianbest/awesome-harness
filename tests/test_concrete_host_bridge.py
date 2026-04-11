import tempfile
import unittest
from pathlib import Path

from bootstrap import HostBridgeLaunchRequest, HostBridgeSessionApi, LaunchMode
from bootstrap.concrete_host_bridge import (
    CLAUDE_HOST_ADAPTER_ID,
    CURSOR_HOST_ADAPTER_ID,
    GarageHostAdapterError,
    OPENCODE_HOST_ADAPTER_ID,
    require_claude_host_bridge,
    require_cursor_host_bridge,
    require_opencode_host_bridge,
)


class ConcreteHostBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_require_cursor_accepts_cursor_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            rh = Path(tmp) / "rh"
            req = HostBridgeLaunchRequest(
                host_adapter_id=CURSOR_HOST_ADAPTER_ID,
                launch_mode=LaunchMode.CREATE,
                source_root=self.repo_root,
                runtime_home=rh,
                workspace_root=ws,
                workspace_id="w",
                profile_id="dogfood",
                problem_kind="implementation",
                entry_pack="coding",
                entry_node="coding.bridge-intake",
                goal="g",
            )
            self.assertIs(require_cursor_host_bridge(req), req)

    def test_require_cursor_rejects_other_host(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            rh = Path(tmp) / "rh"
            req = HostBridgeLaunchRequest(
                host_adapter_id="claude",
                launch_mode=LaunchMode.CREATE,
                source_root=self.repo_root,
                runtime_home=rh,
                workspace_root=ws,
                workspace_id="w",
                profile_id="dogfood",
                problem_kind="implementation",
                entry_pack="coding",
                entry_node="coding.bridge-intake",
                goal="g",
            )
            with self.assertRaises(GarageHostAdapterError):
                require_cursor_host_bridge(req)

    def test_cursor_shell_pipeline_uses_shared_session_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            rh = Path(tmp) / "rh"
            req = require_cursor_host_bridge(
                HostBridgeLaunchRequest(
                    host_adapter_id=CURSOR_HOST_ADAPTER_ID,
                    launch_mode=LaunchMode.CREATE,
                    source_root=self.repo_root,
                    runtime_home=rh,
                    workspace_root=ws,
                    workspace_id="w",
                    profile_id="dogfood",
                    problem_kind="implementation",
                    entry_pack="coding",
                    entry_node="coding.bridge-intake",
                    goal="g",
                )
            )
            result = HostBridgeSessionApi().create(req)
            self.assertEqual(result.services.host.adapter_id, "cursor")

    def test_require_claude_accepts_claude_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            rh = Path(tmp) / "rh"
            req = HostBridgeLaunchRequest(
                host_adapter_id=CLAUDE_HOST_ADAPTER_ID,
                launch_mode=LaunchMode.CREATE,
                source_root=self.repo_root,
                runtime_home=rh,
                workspace_root=ws,
                workspace_id="w",
                profile_id="dogfood",
                problem_kind="implementation",
                entry_pack="coding",
                entry_node="coding.bridge-intake",
                goal="g",
            )
            self.assertIs(require_claude_host_bridge(req), req)

    def test_require_opencode_accepts_opencode_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            rh = Path(tmp) / "rh"
            req = HostBridgeLaunchRequest(
                host_adapter_id=OPENCODE_HOST_ADAPTER_ID,
                launch_mode=LaunchMode.CREATE,
                source_root=self.repo_root,
                runtime_home=rh,
                workspace_root=ws,
                workspace_id="w",
                profile_id="dogfood",
                problem_kind="implementation",
                entry_pack="coding",
                entry_node="coding.bridge-intake",
                goal="g",
            )
            self.assertIs(require_opencode_host_bridge(req), req)


if __name__ == "__main__":
    unittest.main()
