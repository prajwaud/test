"""Snapshot live Graph data to a fixture file.

Why this exists: iterating on the prompt against live Graph calls is slow, rate-limited, and
non-deterministic - the inbox changes under you, so you cannot tell whether an output
changed because of your edit or because new mail arrived. A fixture freezes the input so
prompt changes are the only variable.

    python -m src.capture

CONFIDENTIALITY: fixtures contain real calendar entries and real email previews. They are
gitignored and must stay that way. Do not paste fixture contents into anything external.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import graph_client

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
DISPLAY_TIMEZONE = os.environ.get("BRIEF_DISPLAY_TIMEZONE", "America/New_York")


def latest_fixture() -> Path | None:
    if not FIXTURES_DIR.exists():
        return None
    fixtures = sorted(FIXTURES_DIR.glob("*.json"))
    return fixtures[-1] if fixtures else None


def load_fixture(path: Path) -> tuple[list, list, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("events", []), data.get("messages", []), data.get("meta", {})


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot live Graph data to fixtures/.")
    parser.add_argument("--label", help="Optional suffix, e.g. 'busy-day' or 'empty-inbox'.")
    args = parser.parse_args()

    mailbox = os.environ.get("BRIEF_MAILBOX")
    if not mailbox:
        print("BRIEF_MAILBOX is not set. See ADMIN-ENTRA-REQUEST.md.", file=sys.stderr)
        return 1

    try:
        token = graph_client.get_token()
        events = graph_client.get_todays_events(token, mailbox)
        messages = graph_client.get_unread(token, mailbox)
    except graph_client.GraphError as exc:
        print(f"Capture failed: {exc}", file=sys.stderr)
        return 1

    now = datetime.now(ZoneInfo(DISPLAY_TIMEZONE))
    stem = now.strftime("%Y-%m-%d-%H%M")
    if args.label:
        stem += f"-{args.label}"

    FIXTURES_DIR.mkdir(exist_ok=True)
    path = FIXTURES_DIR / f"{stem}.json"
    path.write_text(json.dumps({
        "meta": {
            "captured_at": now.isoformat(),
            "display_timezone": DISPLAY_TIMEZONE,
            "mailbox": mailbox,
        },
        "events": events,
        "messages": messages,
    }, indent=2), encoding="utf-8")

    print(f"Captured {len(events)} events and {len(messages)} unread to {path}")
    print("Contains real mail content - gitignored, keep it local.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
