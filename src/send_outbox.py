"""Send queued outbox emails via app-only Graph. No human, no prompts.

Why this exists: every send through the Microsoft 365 MCP connector raises an
interactive permission prompt that requires a human click - confirmed repeatedly,
most recently on the 2026-08-28 inaugural digest send. Claude therefore never sends
directly. Instead, Claude sessions (the Friday digest routine, later the daily brief)
assemble the finished email and commit it to outbox/ as JSON; this script, run by
GitHub Actions with app-only Graph credentials, does the actual send.

    python -m src.send_outbox            send everything pending in outbox/
    python -m src.send_outbox --dry-run  validate and print, send nothing

Outbox entry schema (outbox/<name>.json):
    {
      "subject":      str,
      "to":           [str, ...],       validated against outbox/recipients-allowlist.json
      "body":         str,
      "content_type": "HTML" | "Text",  default "HTML"
      "source":       str               free-form provenance, e.g. "cim-scan digest 2026-08-28"
    }

On success an entry is moved to outbox/sent/ with a sent_at stamp - the receipt.
On any failure the entry stays put and the process exits nonzero, so the scheduled
backstop run retries it. Recipients not on the allowlist fail the entry: the queue
is written by an automated session, and a deterministic allowlist is the guard that
keeps a bug or a poisoned input from mailing deal content to an arbitrary address.

UNVERIFIED against live credentials until the Entra app registration exists
(ADMIN-ENTRA-REQUEST.md). Same credential and scopes as the daily brief; Mail.Send
is already in the request. The Application Access Policy restricts which mailbox the
app acts AS (praj@waudcapital.com) - it does not restrict recipients, so digest sends
to Doug and rwaud2 work unchanged.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import graph_client

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTBOX_DIR = REPO_ROOT / "outbox"
SENT_DIR = OUTBOX_DIR / "sent"
ALLOWLIST_PATH = OUTBOX_DIR / "recipients-allowlist.json"


def load_allowlist() -> set[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return {a.strip().lower() for a in data["allowed_recipients"]}


def pending_entries() -> list[Path]:
    if not OUTBOX_DIR.exists():
        return []
    return sorted(p for p in OUTBOX_DIR.glob("*.json")
                  if p.name != ALLOWLIST_PATH.name)


def validate(entry: dict, allowlist: set[str], path: Path) -> list[str]:
    problems = []
    if not entry.get("subject"):
        problems.append("missing subject")
    if not entry.get("body"):
        problems.append("missing body")
    recipients = entry.get("to") or []
    if not recipients:
        problems.append("no recipients")
    for r in recipients:
        if r.strip().lower() not in allowlist:
            problems.append(f"recipient not on allowlist: {r}")
    if entry.get("content_type", "HTML") not in ("HTML", "Text"):
        problems.append(f"bad content_type: {entry.get('content_type')}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Send pending outbox entries via Graph.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate and print, send nothing.")
    args = parser.parse_args()

    entries = pending_entries()
    if not entries:
        print("Outbox empty - nothing to send.")
        return 0

    allowlist = load_allowlist()
    mailbox = os.environ.get("BRIEF_MAILBOX")
    if not mailbox and not args.dry_run:
        print("BRIEF_MAILBOX is not set. See ADMIN-ENTRA-REQUEST.md.", file=sys.stderr)
        return 1

    failures = 0
    token = None if args.dry_run else graph_client.get_token()
    SENT_DIR.mkdir(parents=True, exist_ok=True)

    for path in entries:
        entry = json.loads(path.read_text(encoding="utf-8"))
        problems = validate(entry, allowlist, path)
        if problems:
            print(f"REFUSED {path.name}: {'; '.join(problems)}", file=sys.stderr)
            failures += 1
            continue

        if args.dry_run:
            print(f"WOULD SEND {path.name}: '{entry['subject']}' "
                  f"to {', '.join(entry['to'])}")
            continue

        try:
            graph_client.send_mail(
                token, mailbox,
                subject=entry["subject"],
                body=entry["body"],
                to=entry["to"],
                content_type=entry.get("content_type", "HTML"),
            )
        except graph_client.GraphError as exc:
            print(f"FAILED {path.name}: {exc}", file=sys.stderr)
            failures += 1
            continue

        entry["sent_at"] = datetime.now(timezone.utc).isoformat()
        receipt = SENT_DIR / path.name
        receipt.write_text(json.dumps(entry, indent=2), encoding="utf-8")
        path.unlink()
        print(f"SENT {path.name}: '{entry['subject']}' to {', '.join(entry['to'])}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
