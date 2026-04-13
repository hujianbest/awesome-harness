from __future__ import annotations

import argparse
import json
import sys
from typing import TextIO

from bootstrap.session_api import SessionApi, SessionError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="garage")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--team", required=True)
    create.add_argument("--workspace", required=True)
    create.add_argument("--profile", required=True)

    resume = sub.add_parser("resume")
    resume.add_argument("--session", required=True)

    attach = sub.add_parser("attach")
    attach.add_argument("--session", required=True)
    attach.add_argument("--workspace", required=True)

    step = sub.add_parser("step")
    step.add_argument("--session", required=True)
    step.add_argument("--input", required=True)

    status = sub.add_parser("status")
    status.add_argument("--session", required=True)

    return parser


def execute(argv: list[str], api: SessionApi | None = None, out: TextIO | None = None, err: TextIO | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    api = api or SessionApi()
    out = out or sys.stdout
    err = err or sys.stderr

    try:
        if args.command == "create":
            payload = api.create_session(args.team, args.workspace, args.profile)
        elif args.command == "resume":
            payload = api.resume_session(args.session)
        elif args.command == "attach":
            payload = api.attach_workspace(args.session, args.workspace)
        elif args.command == "step":
            payload = api.submit_step(args.session, args.input)
        elif args.command == "status":
            payload = api.get_status(args.session)
        else:
            raise SessionError("unsupported_command", f"Unsupported command: {args.command}")
    except SessionError as exc:
        err.write(json.dumps(exc.to_dict()))
        return 1

    out.write(json.dumps(payload))
    return 0


def main() -> int:
    return execute(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
