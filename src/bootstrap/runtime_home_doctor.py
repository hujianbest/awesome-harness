from __future__ import annotations


class RuntimeHomeDoctor:
    def check(self, runtime_home: str, has_workspace: bool) -> dict[str, str]:
        if has_workspace:
            return {"status": "ok", "runtime_home": runtime_home}
        return {"status": "warn", "runtime_home": runtime_home, "issue": "workspace_missing"}
