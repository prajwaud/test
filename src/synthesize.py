"""Turn raw Graph data into the brief.

Claude earns its place here and nowhere else in this pipeline: deciding what matters today
is judgment, while reading a calendar is not.

Degrades rather than aborts. A plain unsynthesized brief that arrives beats a perfect brief
that does not, so any failure in the API call falls back to a mechanical rendering.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

DISPLAY_TIMEZONE = os.environ.get("BRIEF_DISPLAY_TIMEZONE", "America/New_York")
TZ_LABEL = os.environ.get("BRIEF_TIMEZONE_LABEL", "ET")
MODEL = os.environ.get("BRIEF_MODEL", "claude-sonnet-5")

SYSTEM_PROMPT = f"""You write a daily executive brief for Prithvi Raj, Chief Data and AI \
Officer at Waud Capital Partners, a Chicago-based middle-market private equity firm.

Write the brief as plain text. No markdown, no bullet characters beyond a leading hyphen.
Under 400 words.

Structure:

TODAY'S MEETINGS
Each meeting on its own line: time range, then subject, then a short second line naming
who is attending and the platform if relevant. Times are already in {TZ_LABEL} - present
them as given and label them {TZ_LABEL}. Do not convert anything. If there are no meetings,
write "No meetings today."

NOTABLE UNREAD
Group under three headings, omitting any heading that has nothing under it:
  ACTION REQUIRED - something is due today, or someone is explicitly blocked on him
  NEEDS A REPLY - a direct question to him that is not time-critical
  FYI - useful to know, no action
Each item: sender email, then subject, then one line on why it matters.

Judgment rules:
- Demote vendor cold outreach and automated digests to a single combined FYI line. Do not
  give them individual entries.
- Promote anything with a deadline, a signature request, or a senior colleague waiting.
- Firm context: Reeve Waud Jr. and Doug Rassner are senior. Portfolio companies include
  Ivy Rehab, Altocare, TeamSnap, Apotheco, Talogy, Career Certified, HSI, PracticeTek and
  others. Mail touching a portco or an active workstream outranks internal admin.
- Say what the sender needs, not just that they wrote. "Abbe needs attendee contacts before
  she can schedule" beats "Abbe replied about Summits."
- If nothing qualifies, write "No notable unread." Do not manufacture significance.

Never invent detail that is not in the input."""


def _format_events(events: list[dict[str, Any]]) -> str:
    if not events:
        return "(no events)"
    lines = []
    for e in events:
        start = e.get("start", {}).get("dateTime", "")[:16]
        end = e.get("end", {}).get("dateTime", "")[11:16]
        attendees = ", ".join(
            a.get("emailAddress", {}).get("address", "")
            for a in (e.get("attendees") or [])
        ) or "(none listed)"
        location = (e.get("location") or {}).get("displayName") or "(no location)"
        lines.append(
            f"- {start} to {end} | {e.get('subject', '(no subject)')} | "
            f"location: {location} | attendees: {attendees}"
        )
    return "\n".join(lines)


def _format_unread(messages: list[dict[str, Any]]) -> str:
    if not messages:
        return "(no unread)"
    lines = []
    for m in messages:
        sender = m.get("from", {}).get("emailAddress", {}).get("address", "(unknown)")
        preview = (m.get("bodyPreview") or "").replace("\r", " ").replace("\n", " ")[:300]
        flags = []
        if m.get("importance") == "high":
            flags.append("high importance")
        if m.get("hasAttachments"):
            flags.append("has attachments")
        suffix = f" [{', '.join(flags)}]" if flags else ""
        lines.append(
            f"- from: {sender} | subject: {m.get('subject', '(no subject)')}{suffix}\n"
            f"  preview: {preview}"
        )
    return "\n".join(lines)


def _fallback(events: list[dict[str, Any]], messages: list[dict[str, Any]]) -> str:
    """Mechanical rendering used when the API call fails. Ugly but never silent."""
    parts = ["(Synthesis unavailable - raw data below.)", "", "TODAY'S MEETINGS", ""]
    parts.append(_format_events(events))
    parts += ["", "UNREAD", "", _format_unread(messages)]
    return "\n".join(parts)


def build_brief(events: list[dict[str, Any]],
                messages: list[dict[str, Any]]) -> str:
    """Return the brief body. Never raises."""
    now = datetime.now(ZoneInfo(DISPLAY_TIMEZONE))
    header = (
        f"Generated {now.strftime('%Y-%m-%d %H:%M')} {TZ_LABEL}\n"
        f"{len(events)} meetings, {len(messages)} unread\n"
    )

    user_content = (
        f"Today is {now.strftime('%A, %B %d, %Y')}. "
        f"All times below are already in {TZ_LABEL}.\n\n"
        f"CALENDAR EVENTS:\n{_format_events(events)}\n\n"
        f"UNREAD MESSAGES:\n{_format_unread(messages)}"
    )

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        return header + "\n" + response.content[0].text
    except Exception as exc:  # noqa: BLE001 - degrading is the point
        return header + "\n" + f"(Synthesis failed: {exc})\n\n" + _fallback(events, messages)
