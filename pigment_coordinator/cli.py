import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

from .engine import Coordinator
from .errors import CoordinatorError
from .providers import FakeProvider, providers_from_environment


def default_validator() -> str:
    configured = os.environ.get("PIGMENT_VALIDATOR_COMMAND")
    if configured is not None:
        return configured
    if shutil.which("node"):
        return "node tools/validate.js"
    if shutil.which("osascript"):
        return "osascript -l JavaScript tools/validate.jxa.js"
    return ""


def build_coordinator(repo_root: Path, fake: bool, require_providers: bool) -> Coordinator:
    if require_providers:
        theory, synthesis, build = providers_from_environment(repo_root, fake=fake)
    else:
        theory = synthesis = build = FakeProvider()
    return Coordinator(repo_root, theory, synthesis, build, default_validator())


def print_state(state: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(state, indent=2, sort_keys=True))
        return
    print(f"{state['task_id']}: {state['workflow_state']}")
    print(f"Objective: {state['objective']}")
    print(f"Round: {state['round']}/{state['max_rounds']}")
    print(f"Provider calls: {state['provider_calls']}/{state['max_provider_calls']}")
    print(f"Messages: {state['message_count']}")
    print(f"Analyst packets: {state.get('analyst_count', 0)}")
    print(f"Build authorized: {'yes' if state['build_authorized'] else 'no'}")
    if state.get("human_decision"):
        print(f"Human decision: {state['human_decision']['decision']}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Neutral Pigment dipolar-team Coordinator")
    result.add_argument("--repo", default=".", help="Pigment repository root")
    result.add_argument("--fake", action="store_true", help="Use deterministic no-cost providers")
    result.add_argument("--json", action="store_true", help="Print full JSON state")
    commands = result.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="Open a new objective")
    create.add_argument("task_id")
    create.add_argument("objective")
    create.add_argument("--max-rounds", type=int, default=3)
    create.add_argument("--max-provider-calls", type=int, default=20)

    adopt = commands.add_parser(
        "adopt",
        help="Register an existing task directory at intake, preserving its pre-kernel artifacts under unrouted/",
    )
    adopt.add_argument("task_id")
    adopt.add_argument("objective")
    adopt.add_argument("--baseline", required=True, help="Commit identifier the recovered task is rebaselined against")
    adopt.add_argument("--max-rounds", type=int, default=3)
    adopt.add_argument("--max-provider-calls", type=int, default=20)

    ingest = commands.add_parser(
        "ingest",
        help="Route an externally produced deliberation message (JSON) with its liaison audit packet",
    )
    ingest.add_argument("task_id")
    ingest.add_argument("message", help="Path to the message JSON file")
    ingest.add_argument("--analyst", required=True, help="Path to the liaison analyst packet JSON file")

    for name, help_text in (
        ("advance", "Run exactly one deterministic transition"),
        ("run", "Run until a human or configuration pause"),
        ("status", "Show task state"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("task_id")

    approve = commands.add_parser("approve", help="Record the product owner's approval")
    approve.add_argument("task_id")
    approve.add_argument("--note", default="")

    reject = commands.add_parser("reject", help="Record the product owner's rejection")
    reject.add_argument("task_id")
    reject.add_argument("--note", default="")
    return result


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    repo_root = Path(args.repo).resolve()
    require_providers = args.command in ("advance", "run")
    try:
        coordinator = build_coordinator(repo_root, args.fake, require_providers)
        if args.command == "create":
            state = coordinator.create_task(
                args.task_id,
                args.objective,
                args.max_rounds,
                args.max_provider_calls,
            )
        elif args.command == "adopt":
            state = coordinator.adopt_task(
                args.task_id,
                args.objective,
                args.baseline,
                args.max_rounds,
                args.max_provider_calls,
            )
        elif args.command == "ingest":
            state = coordinator.ingest(args.task_id, Path(args.message), Path(args.analyst))
        elif args.command == "advance":
            state = coordinator.advance(args.task_id)
        elif args.command == "run":
            state = coordinator.run_until_pause(args.task_id)
        elif args.command == "status":
            state = coordinator.status(args.task_id)
        elif args.command == "approve":
            state = coordinator.decide(args.task_id, "approved", args.note)
        elif args.command == "reject":
            state = coordinator.decide(args.task_id, "rejected", args.note)
        else:
            raise AssertionError(args.command)
        print_state(state, args.json)
        return 0
    except CoordinatorError as exc:
        print(f"Coordinator stopped: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
