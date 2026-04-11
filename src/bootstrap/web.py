"""Local-first WebEntry control plane built on the shared SessionApi seam."""

from __future__ import annotations

import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any, Mapping

from .launcher import BootstrapConfig, BootstrapError, LaunchMode
from .session_api import SessionApi


@dataclass(slots=True, frozen=True)
class WebControlPlaneConfig:
    host: str = "127.0.0.1"
    port: int = 0


@dataclass(slots=True, frozen=True)
class WebControlPlaneState:
    bind_host: str
    port: int

    @property
    def base_url(self) -> str:
        return f"http://{self.bind_host}:{self.port}"


class WebControlPlane:
    """Minimal local-first web control plane with health and session endpoints."""

    def __init__(
        self,
        session_api: SessionApi | None = None,
        config: WebControlPlaneConfig | None = None,
    ) -> None:
        self._session_api = session_api or SessionApi()
        self._config = config or WebControlPlaneConfig()
        self._server: ThreadingHTTPServer | None = None
        self._thread: Thread | None = None

    def start(self) -> WebControlPlaneState:
        if self._server is not None:
            raise RuntimeError("Web control plane is already running.")
        handler_type = self._build_handler()
        server = ThreadingHTTPServer((self._config.host, self._config.port), handler_type)
        thread = Thread(target=server.serve_forever, name="garage-web-control-plane", daemon=True)
        thread.start()
        self._server = server
        self._thread = thread
        return WebControlPlaneState(bind_host=server.server_address[0], port=server.server_address[1])

    def stop(self) -> None:
        if self._server is None:
            return
        self._server.shutdown()
        self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._server = None
        self._thread = None

    def _build_handler(self) -> type[BaseHTTPRequestHandler]:
        session_api = self._session_api

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                if self.path == "/health":
                    self._write_json(
                        HTTPStatus.OK,
                        {
                            "status": "healthy",
                            "entrySurface": "web",
                            "hostAdapterId": "web",
                        },
                    )
                    return
                self._write_json(HTTPStatus.NOT_FOUND, {"error": "unknown-endpoint"})

            def do_POST(self) -> None:  # noqa: N802
                try:
                    payload = self._read_json_body()
                    if self.path == "/sessions/create":
                        result = session_api.create(_bootstrap_config_from_web_payload(payload, LaunchMode.CREATE))
                    elif self.path == "/sessions/resume":
                        result = session_api.resume(_bootstrap_config_from_web_payload(payload, LaunchMode.RESUME))
                    elif self.path == "/sessions/attach":
                        result = session_api.attach(_bootstrap_config_from_web_payload(payload, LaunchMode.ATTACH))
                    else:
                        self._write_json(HTTPStatus.NOT_FOUND, {"error": "unknown-endpoint"})
                        return
                    self._write_json(HTTPStatus.OK, session_api.summarize(result).as_mapping())
                except (BootstrapError, ValueError) as exc:
                    self._write_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})

            def log_message(self, format: str, *args: object) -> None:
                return

            def _read_json_body(self) -> Mapping[str, Any]:
                content_length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(content_length)
                if not raw:
                    return {}
                return json.loads(raw.decode("utf-8"))

            def _write_json(self, status: HTTPStatus, payload: Mapping[str, Any]) -> None:
                encoded = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

        return Handler


def _bootstrap_config_from_web_payload(payload: Mapping[str, Any], launch_mode: LaunchMode) -> BootstrapConfig:
    common_kwargs = {
        "source_root": Path(_require_str(payload, "sourceRoot")),
        "runtime_home": Path(_require_str(payload, "runtimeHome")),
        "workspace_root": Path(_require_str(payload, "workspaceRoot")),
        "workspace_id": payload.get("workspaceId"),
        "profile_id": payload.get("profileId", "default"),
        "entry_surface": "web",
        "host_adapter_id": payload.get("hostAdapterId"),
        "session_id": payload.get("sessionId"),
        "initiator": payload.get("initiator", "creator"),
    }
    if launch_mode == LaunchMode.CREATE:
        return BootstrapConfig(
            launch_mode=launch_mode,
            problem_kind=_require_str(payload, "problemKind"),
            entry_pack=_require_str(payload, "entryPack"),
            entry_node=_require_str(payload, "entryNode"),
            goal=_require_str(payload, "goal"),
            summary=payload.get("summary"),
            boundaries=tuple(payload.get("boundaries", ())),
            **common_kwargs,
        )
    return BootstrapConfig(launch_mode=launch_mode, **common_kwargs)


def _require_str(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Web control plane requires a non-empty {key}.")
    return value
