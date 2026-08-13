"""Microsoft Graph client using app-only (client credentials) authentication.

No user context, no browser, no refresh token. See docs/ARCHITECTURE.md for why.

UNVERIFIED: written against the documented Graph contract but never run against live
credentials, because the Entra app registration does not exist yet. Do not describe this
as working until a --dry-run has succeeded.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_HOST = "https://login.microsoftonline.com"

# The mailbox timezone. Graph returns calendar wall-clock times in whatever timezone we
# ask for via the Prefer header, which is more reliable than converting after the fact.
MAILBOX_TIMEZONE = os.environ.get("BRIEF_MAILBOX_TIMEZONE", "America/Chicago")

# What the reader sees. Kept separate from MAILBOX_TIMEZONE because these may differ -
# see the unresolved timezone question in docs/TEST-LOG.md.
DISPLAY_TIMEZONE = os.environ.get("BRIEF_DISPLAY_TIMEZONE", "America/New_York")


class GraphError(RuntimeError):
    """Raised with enough context to diagnose without re-running."""


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise GraphError(
            f"{name} is not set. All four of GRAPH_TENANT_ID, GRAPH_CLIENT_ID, "
            f"GRAPH_CLIENT_SECRET and BRIEF_MAILBOX are required. "
            f"See ADMIN-ENTRA-REQUEST.md for how to obtain them."
        )
    return value


def get_token() -> str:
    """Mint a fresh access token. Called once per run, so no caching needed."""
    tenant_id = _require_env("GRAPH_TENANT_ID")
    resp = requests.post(
        f"{TOKEN_HOST}/{tenant_id}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "client_id": _require_env("GRAPH_CLIENT_ID"),
            "client_secret": _require_env("GRAPH_CLIENT_SECRET"),
            "scope": "https://graph.microsoft.com/.default",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise GraphError(
            f"Token request failed ({resp.status_code}). A 401 here usually means an "
            f"expired or mistyped client secret. Response: {resp.text[:500]}"
        )
    return resp.json()["access_token"]


def _get(token: str, path: str, params: dict[str, Any] | None = None,
         prefer: str | None = None) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    if prefer:
        headers["Prefer"] = prefer

    for attempt in range(4):
        resp = requests.get(f"{GRAPH_BASE}{path}", headers=headers,
                            params=params, timeout=60)

        if resp.status_code == 429:
            # Honour Retry-After rather than guessing.
            wait = int(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue

        if resp.status_code == 403:
            raise GraphError(
                f"403 Forbidden on {path}. The app registration most likely lacks admin "
                f"consent, or the Application Access Policy excludes this mailbox. "
                f"Verify with: Test-ApplicationAccessPolicy -Identity <mailbox> "
                f"-AppId <client-id>. Response: {resp.text[:500]}"
            )

        if resp.status_code != 200:
            raise GraphError(f"GET {path} failed ({resp.status_code}): {resp.text[:500]}")

        return resp.json()

    raise GraphError(f"GET {path} still throttled after 4 attempts.")


def get_todays_events(token: str, mailbox: str) -> list[dict[str, Any]]:
    """Today's calendar events, as wall-clock times in DISPLAY_TIMEZONE.

    Uses calendarView rather than /events so that recurring-series instances are expanded
    into concrete occurrences. Plain /events returns the series master and would miss
    today's instance of a weekly meeting.
    """
    now_local = datetime.now(ZoneInfo(DISPLAY_TIMEZONE))
    start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    payload = _get(
        token,
        f"/users/{mailbox}/calendarView",
        params={
            "startDateTime": start.isoformat(),
            "endDateTime": end.isoformat(),
            "$select": "subject,start,end,location,attendees,organizer,isCancelled,showAs",
            "$orderby": "start/dateTime",
            "$top": "50",
        },
        # Ask Graph to return times already in the display timezone. This is the fix for
        # the mailbox-is-Central / display-is-Eastern mismatch: convert once, at the API
        # boundary, instead of doing arithmetic downstream.
        prefer=f'outlook.timezone="{DISPLAY_TIMEZONE}"',
    )

    return [e for e in payload.get("value", []) if not e.get("isCancelled")]


def get_unread(token: str, mailbox: str, hours: int = 24) -> list[dict[str, Any]]:
    """Unread inbox messages from the last `hours`.

    Filters unread server-side. The MCP connector had no unread filter and required
    client-side filtering on isRead; Graph does not.
    """
    since = (datetime.now(ZoneInfo("UTC")) - timedelta(hours=hours))
    since_str = since.strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = _get(
        token,
        f"/users/{mailbox}/mailFolders/inbox/messages",
        params={
            "$filter": f"isRead eq false and receivedDateTime ge {since_str}",
            "$select": "subject,from,toRecipients,receivedDateTime,bodyPreview,importance,hasAttachments",
            "$orderby": "receivedDateTime desc",
            "$top": "50",
        },
    )
    return payload.get("value", [])


def send_mail(token: str, mailbox: str, subject: str, body: str,
              to: str | None = None) -> None:
    """Send plain text mail from and to the given mailbox."""
    recipient = to or mailbox
    resp = requests.post(
        f"{GRAPH_BASE}/users/{mailbox}/sendMail",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "message": {
                "subject": subject,
                "body": {"contentType": "Text", "content": body},
                "toRecipients": [{"emailAddress": {"address": recipient}}],
            },
            "saveToSentItems": True,
        },
        timeout=60,
    )
    if resp.status_code not in (200, 202):
        raise GraphError(
            f"sendMail failed ({resp.status_code}). A 403 here means Mail.Send is not "
            f"consented, or the access policy blocks this mailbox. "
            f"Response: {resp.text[:500]}"
        )
