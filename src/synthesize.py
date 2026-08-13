"""Turn raw Graph data into the brief.

Claude earns its place here and nowhere else in this pipeline. Reading a calendar is
mechanical; deciding that a buried execution link is today's real obligation is judgment.

The prompt lives in prompts/system.md, not in this file. See src/prompt_loader.py.

Degrades rather than aborts: a plain unsynthesized brief that arrives beats a perfect brief
that does not, so failure in the API call falls back to a mechanical rendering.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from . import prompt_loader
from .formatting import build_user_content, format_events, format_unread

DISPLAY_TIMEZONE = os.environ.get("BRIEF_DISPLAY_TIMEZONE", "America/New_York")
TZ_LABEL = os.environ.get("BRIEF_TIMEZONE_LABEL", "ET")


@dataclass
class Synthesis:
    """Result of one synthesis attempt, including what it cost and whether it degraded."""
    body: str
    prompt_name: str
    prompt_version: Any
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    degraded: bool = False
    error: str | None = None

    def cost_note(self) -> str:
        if self.degraded:
            return "degraded, no API call billed"
        return f"{self.input_tokens} in / {self.output_tokens} out"


def _fallback(events: list[dict[str, Any]], messages: list[dict[str, Any]]) -> str:
    """Mechanical rendering. Ugly, but never silent."""
    return "\n".join([
        "(Synthesis unavailable - raw data below.)",
        "",
        "TODAY'S MEETINGS",
        "",
        format_events(events),
        "",
        "UNREAD",
        "",
        format_unread(messages),
    ])


def synthesize(events: list[dict[str, Any]],
               messages: list[dict[str, Any]],
               prompt_name: str = "system",
               now: datetime | None = None) -> Synthesis:
    """Run one synthesis. Never raises - failures come back as degraded results."""
    now = now or datetime.now(ZoneInfo(DISPLAY_TIMEZONE))
    prompt = prompt_loader.load(prompt_name)
    system = prompt.render(tz_label=TZ_LABEL)

    user_content = build_user_content(
        events, messages,
        date_label=now.strftime("%A, %B %d, %Y"),
        tz_label=TZ_LABEL,
    )

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model=prompt.model,
            max_tokens=prompt.max_tokens,
            temperature=prompt.temperature,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
        return Synthesis(
            body=response.content[0].text,
            prompt_name=prompt.name,
            prompt_version=prompt.version,
            model=prompt.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
    except Exception as exc:  # noqa: BLE001 - degrading is the entire point
        return Synthesis(
            body=_fallback(events, messages),
            prompt_name=prompt.name,
            prompt_version=prompt.version,
            model=prompt.model,
            degraded=True,
            error=f"{type(exc).__name__}: {exc}",
        )


def build_brief(events: list[dict[str, Any]],
                messages: list[dict[str, Any]],
                prompt_name: str = "system") -> str:
    """Full email body including header. Convenience wrapper for the live run."""
    now = datetime.now(ZoneInfo(DISPLAY_TIMEZONE))
    result = synthesize(events, messages, prompt_name=prompt_name, now=now)

    header = (
        f"Generated {now.strftime('%Y-%m-%d %H:%M')} {TZ_LABEL}\n"
        f"{len(events)} meetings, {len(messages)} unread"
    )
    if result.degraded:
        header += f"\nNOTE: synthesis degraded - {result.error}"

    return f"{header}\n\n{result.body}"
