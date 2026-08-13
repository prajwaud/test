"""Render raw Graph payloads into the plain-text blocks the model reads.

Kept separate from synthesis so that fixtures, tuning and the live run all feed the model
byte-identical input. If this drifted per caller, tuning results would not transfer to
production.
"""

from __future__ import annotations

from typing import Any


def format_events(events: list[dict[str, Any]]) -> str:
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


def format_unread(messages: list[dict[str, Any]]) -> str:
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


def build_user_content(events: list[dict[str, Any]],
                       messages: list[dict[str, Any]],
                       date_label: str,
                       tz_label: str) -> str:
    return (
        f"Today is {date_label}. All times below are already in {tz_label}.\n\n"
        f"CALENDAR EVENTS:\n{format_events(events)}\n\n"
        f"UNREAD MESSAGES:\n{format_unread(messages)}"
    )
