from __future__ import annotations

import argparse
import json
import sys

from .config import Settings
from .manager import GovernanceBlocker, Manager


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="anandtech-agents")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Print current workflow state")

    draft = commands.add_parser("draft-ssot", help="Ask the SSOT Maker to draft or revise the active section")
    draft.add_argument("--brief", required=True)

    lock = commands.add_parser("lock-ssot", help="Human-only explicit SSOT lock")
    lock.add_argument("--confirmation", required=True)
    lock.add_argument("--approved-by", required=True)

    commands.add_parser("run-section", help="Run the bounded Worker/Reviewer loop")
    commands.add_parser("retry-notifications", help="Retry pending Slack events without changing curriculum state")

    accept = commands.add_parser("accept-section", help="Human-only final section acceptance")
    accept.add_argument("--confirmation", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    manager = Manager(Settings.from_environment())
    try:
        if args.command == "status":
            print(json.dumps(manager.status(), indent=2, ensure_ascii=False))
        elif args.command == "draft-ssot":
            print("Updated: " + ", ".join(manager.draft_ssot(args.brief)))
        elif args.command == "lock-ssot":
            manager.lock_ssot(args.confirmation, args.approved_by)
            print("Section SSOT locked; generation is now authorized.")
        elif args.command == "run-section":
            manager.run_section()
            print("All units approved; waiting for owner confirmation.")
        elif args.command == "retry-notifications":
            manager.retry_notifications()
            print("Eligible Slack events processed; inspect status for delivery state.")
        elif args.command == "accept-section":
            manager.accept_section(args.confirmation)
            print("Section accepted. The next SSOT may now be drafted.")
    except (GovernanceBlocker, RuntimeError, ValueError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
