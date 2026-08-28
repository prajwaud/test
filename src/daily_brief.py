"""Entry point for the daily brief.

    python -m src.daily_brief --dry-run   read live data, print, send nothing
    python -m src.daily_brief             read, synthesize, send
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from . import graph_client
from .synthesize import build_brief

DISPLAY_TIMEZONE = os.environ.get("BRIEF_DISPLAY_TIMEZONE", "America/New_York")
TARGET_HOUR = int(os.environ.get("BRIEF_TARGET_HOUR", "5"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Send the daily executive brief.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Read and synthesize, print to stdout, send nothing.")
    parser.add_argument("--enforce-hour", action="store_true",
                        help="Exit 0 without doing anything unless the local hour matches "
                             "BRIEF_TARGET_HOUR. Used by the scheduled runner so two cron "
                             "entries can bracket DST without double-sending.")
    args = parser.parse_args()

    now = datetime.now(ZoneInfo(DISPLAY_TIMEZONE))

    if args.enforce_hour and now.hour != TARGET_HOUR:
        print(f"Local hour is {now.hour}, target is {TARGET_HOUR}. Nothing to do.")
        return 0

    mailbox = os.environ.get("BRIEF_MAILBOX")
    if not mailbox:
        print("BRIEF_MAILBOX is not set. See ADMIN-ENTRA-REQUEST.md.", file=sys.stderr)
        return 1

    try:
        token = graph_client.get_token()
        events = graph_client.get_todays_events(token, mailbox)
        messages = graph_client.get_unread(token, mailbox)
    except graph_client.GraphError as exc:
        # Read failures are fatal and loud. There is nothing worth sending.
        print(f"Graph read failed: {exc}", file=sys.stderr)
        return 1

    body = build_brief(events, messages)
    subject = f"Daily Brief - {now.strftime('%B %d, %Y')}"

    if args.dry_run:
        print(f"--- DRY RUN, nothing sent ---\nSubject: {subject}\n")
        print(body)
        print("\n--- verify the meeting times against the real calendar before trusting "
              "this. See the timezone note in docs/TEST-LOG.md. ---")
        return 0

    # Reads come from Prithvi's mailbox; the send goes out from the agent mailbox when
    # one is configured (SEND_MAILBOX), so all automated mail shares one sender identity.
    send_from = os.environ.get("SEND_MAILBOX", mailbox)
    try:
        graph_client.send_mail(token, send_from, subject, body, to=mailbox)
    except graph_client.GraphError as exc:
        print(f"Send failed: {exc}", file=sys.stderr)
        return 1

    print(f"Sent: {subject} ({len(events)} meetings, {len(messages)} unread)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
