import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bootstrap import (
    BootstrapConfig,
    CredentialResolutionError,
    GarageLauncher,
    LaunchMode,
    RuntimeProfileResolutionError,
    load_runtime_profile,
    merge_credential_ref_declarations,
    resolve_credential_refs,
)
from foundation import RuntimeHomeBinding


class CredentialResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_merge_profile_overrides_adapter_order(self) -> None:
        merged = merge_credential_ref_declarations(
            {"credentials": {"apiKey": "env:FROM_PROFILE"}},
            {"credentials": {"apiKey": "env:FROM_OVERRIDE"}},
            {"credentials": {"apiKey": "env:FROM_DEFAULT"}},
            {"apiKeyRef": "env:FROM_ADAPTER"},
        )
        self.assertEqual(merged["apiKey"], "env:FROM_PROFILE")

    def test_same_layer_conflict_credentials_and_ref(self) -> None:
        with self.assertRaises(CredentialResolutionError):
            merge_credential_ref_declarations(
                {"credentials": {"apiKey": "env:A"}, "apiKeyRef": "env:B"},
                {},
                {},
                {},
            )

    def test_resolve_env_ref(self) -> None:
        rh = RuntimeHomeBinding.from_root(Path("/tmp/garage-rh"))
        with mock.patch.dict(os.environ, {"GARAGE_TEST_TOKEN": "secret-value-12345678"}):
            resolved = resolve_credential_refs({"token": "env:GARAGE_TEST_TOKEN"}, rh)
        self.assertEqual(resolved.values["token"], "secret-value-12345678")

    def test_resolve_runtime_config_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            cfg = root / "config" / "secrets"
            cfg.mkdir(parents=True)
            (cfg / "tok.txt").write_text("  file-secret-12345678  \n", encoding="utf-8")
            rh = RuntimeHomeBinding.from_root(root)
            resolved = resolve_credential_refs({"tok": "runtime-config:secrets/tok.txt"}, rh)
            self.assertEqual(resolved.values["tok"], "file-secret-12345678")

    def test_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            (root / "config").mkdir(parents=True)
            rh = RuntimeHomeBinding.from_root(root)
            with self.assertRaises(CredentialResolutionError):
                resolve_credential_refs({"x": "runtime-config:../outside.txt"}, rh)

    def test_launcher_resolves_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_home_root = Path(tmp_dir) / "runtime-home"
            workspace_root = Path(tmp_dir) / "workspace"
            self._write_json(
                runtime_home_root / "profiles" / "dogfood.json",
                {
                    "providerId": "provider.dogfood",
                    "modelId": "model.dogfood",
                    "adapterId": "adapter.dogfood",
                    "credentials": {"apiKey": "env:GARAGE_DOGFOOD_KEY"},
                },
            )
            self._write_json(
                runtime_home_root / "adapters" / "adapter.dogfood.json",
                {"providerId": "provider.dogfood"},
            )
            with mock.patch.dict(os.environ, {"GARAGE_DOGFOOD_KEY": "resolved-key-12345678"}):
                result = GarageLauncher().launch(
                    BootstrapConfig(
                        launch_mode=LaunchMode.CREATE,
                        source_root=self.repo_root,
                        runtime_home=runtime_home_root,
                        workspace_root=workspace_root,
                        workspace_id="garage-workspace",
                        profile_id="dogfood",
                        entry_surface="cli",
                        problem_kind="implementation",
                        entry_pack="coding",
                        entry_node="coding.bridge-intake",
                        goal="Credential resolution smoke.",
                    )
                )
            self.assertEqual(result.services.resolved_credentials.values["apiKey"], "resolved-key-12345678")

    def test_profile_loader_wraps_merge_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_home_root = Path(tmp_dir) / "runtime-home"
            self._write_json(
                runtime_home_root / "profiles" / "bad.json",
                {
                    "providerId": "p",
                    "adapterId": "a",
                    "credentials": {"k": "env:X"},
                    "kRef": "env:Y",
                },
            )
            with self.assertRaises(RuntimeProfileResolutionError):
                load_runtime_profile(
                    RuntimeHomeBinding.from_root(runtime_home_root),
                    profile_id="bad",
                )

    @staticmethod
    def _write_json(path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
