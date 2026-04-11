import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bootstrap import DoctorSeverity, diagnose_runtime_home


class RuntimeHomeDoctorTests(unittest.TestCase):
    def test_ok_when_profile_adapter_and_credentials_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            for sub in ("profiles", "config", "adapters", "cache"):
                (root / sub).mkdir(parents=True)
            (root / "profiles" / "p.json").write_text(
                json.dumps(
                    {
                        "providerId": "provider.x",
                        "modelId": "model.x",
                        "adapterId": "adapter.x",
                        "credentials": {"k": "env:GARAGE_DOC_K"},
                    }
                ),
                encoding="utf-8",
            )
            (root / "adapters" / "adapter.x.json").write_text(
                json.dumps({"providerId": "provider.x"}),
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"GARAGE_DOC_K": "secret-1234567890"}):
                findings, ok = diagnose_runtime_home(root, profile_id="p")
            self.assertTrue(ok)
            self.assertFalse(any(f.severity == DoctorSeverity.ERROR for f in findings))

    def test_error_when_profile_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            (root / "profiles").mkdir(parents=True)
            findings, ok = diagnose_runtime_home(root, profile_id="nope")
            self.assertFalse(ok)
            self.assertTrue(any(f.code == "profile.missing" for f in findings))

    def test_error_when_providers_json_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            (root / "profiles").mkdir(parents=True)
            (root / "config").mkdir(parents=True)
            (root / "config" / "providers.json").write_text("{not json", encoding="utf-8")
            (root / "profiles" / "p.json").write_text(json.dumps({"providerId": "x"}), encoding="utf-8")
            findings, ok = diagnose_runtime_home(root, profile_id="p")
            self.assertFalse(ok)
            self.assertTrue(any(f.code == "config.providers_invalid" for f in findings))

    def test_migration_hint_when_version_file_mismatched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "rh"
            for sub in ("profiles", "config", "adapters", "cache"):
                (root / sub).mkdir(parents=True)
            (root / "config" / "runtime-home-version").write_text("0\n", encoding="utf-8")
            (root / "profiles" / "p.json").write_text(json.dumps({"providerId": "x"}), encoding="utf-8")
            findings, ok = diagnose_runtime_home(root, profile_id="p")
            self.assertTrue(ok)
            self.assertTrue(any(f.code == "migration.version_mismatch" for f in findings))


if __name__ == "__main__":
    unittest.main()
