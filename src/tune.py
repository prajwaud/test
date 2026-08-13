"""Iterate on the brief's inference without sending anything.

This is the loop for improving the brief over time:

    python -m src.capture                          snapshot today's real data, once
    # edit prompts/system.md
    python -m src.tune                             replay that snapshot, see the new output
    python -m src.tune --compare system,tighter    same data, two prompts, side by side

Nothing here sends email or touches the calendar. It is read-only against a frozen fixture,
so you can iterate as many times as you like without waiting for 5am or changing the input
under yourself.

    python -m src.tune --save     also write the output to runs/, to diff later
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from . import prompt_loader
from .capture import latest_fixture, load_fixture
from .synthesize import synthesize

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


def _render(result, elapsed: float) -> str:
    head = (
        f"prompt: {result.prompt_name} (v{result.prompt_version})  "
        f"model: {result.model}  "
        f"tokens: {result.cost_note()}  "
        f"{elapsed:.1f}s"
    )
    if result.degraded:
        head += f"\nDEGRADED: {result.error}"
    return f"{head}\n{'-' * len(head.splitlines()[0])}\n{result.body}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replay a fixture through one or more prompts. Sends nothing.")
    parser.add_argument("--fixture", type=Path,
                        help="Fixture to replay. Defaults to the most recent in fixtures/.")
    parser.add_argument("--prompt", default="system",
                        help="Prompt variant to use. Default: system.")
    parser.add_argument("--compare",
                        help="Comma-separated prompt names to run on the same fixture.")
    parser.add_argument("--save", action="store_true",
                        help="Also write output to runs/ for later diffing.")
    parser.add_argument("--list", action="store_true",
                        help="List available prompt variants and exit.")
    args = parser.parse_args()

    if args.list:
        for name in prompt_loader.available():
            p = prompt_loader.load(name)
            status = p.meta.get("status", "-")
            print(f"{name:20} v{p.version:<6} {p.model:20} {status}")
        return 0

    fixture = args.fixture or latest_fixture()
    if not fixture:
        print("No fixture found. Run: python -m src.capture", file=sys.stderr)
        return 1
    if not fixture.exists():
        print(f"No such fixture: {fixture}", file=sys.stderr)
        return 1

    events, messages, meta = load_fixture(fixture)
    print(f"Fixture: {fixture.name}  "
          f"({len(events)} events, {len(messages)} unread, "
          f"captured {meta.get('captured_at', 'unknown')})\n")

    names = [n.strip() for n in args.compare.split(",")] if args.compare else [args.prompt]

    # Check placeholders before spending any tokens - a typo'd {{token}} is otherwise
    # invisible until you read the output closely.
    for name in names:
        try:
            unfilled = set(prompt_loader.load(name).unfilled_placeholders()) - {"tz_label"}
        except FileNotFoundError as exc:
            print(exc, file=sys.stderr)
            return 1
        if unfilled:
            print(f"WARNING: {name}.md has unrecognized placeholders: "
                  f"{', '.join(sorted(unfilled))}", file=sys.stderr)

    for name in names:
        started = datetime.now()
        result = synthesize(events, messages, prompt_name=name)
        elapsed = (datetime.now() - started).total_seconds()

        print("=" * 78)
        print(_render(result, elapsed))
        print()

        if args.save:
            RUNS_DIR.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            out = RUNS_DIR / f"{stamp}-{name}-{fixture.stem}.txt"
            out.write_text(_render(result, elapsed), encoding="utf-8")
            print(f"saved: {out}\n")

    if len(names) > 1:
        print("Read both above and decide which is better. There is no automated judge "
              "here on purpose - you are the evaluator, and what counts as a good brief "
              "is your call, not a metric.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
