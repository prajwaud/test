"""Load editable prompts from prompts/*.md.

The point of this module: the synthesis prompt is prose, and prose is what needs the most
iteration. Keeping it in a markdown file rather than a Python string means it can be edited,
diffed, reviewed and reverted without touching code.

File format is YAML frontmatter plus a markdown body:

    ---
    version: 1
    model: claude-sonnet-5
    max_tokens: 2000
    ---
    You write a daily executive brief for...

Placeholders use double braces - {{tz_label}} - so that literal single braces in the prose
are never mangled.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


@dataclass
class Prompt:
    name: str
    text: str
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def model(self) -> str:
        return self.meta.get("model", "claude-sonnet-5")

    @property
    def max_tokens(self) -> int:
        return int(self.meta.get("max_tokens", 2000))

    @property
    def temperature(self) -> float:
        return float(self.meta.get("temperature", 1.0))

    @property
    def version(self) -> Any:
        return self.meta.get("version", "unversioned")

    def render(self, **values: Any) -> str:
        """Substitute {{placeholder}} tokens. Unknown placeholders are left untouched so a
        typo is visible in the output rather than silently blanked."""
        text = self.text
        for key, value in values.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text

    def unfilled_placeholders(self) -> list[str]:
        return sorted(set(re.findall(r"\{\{(\w+)\}\}", self.text)))


def available() -> list[str]:
    """Every prompt variant on disk, live one first."""
    names = sorted(p.stem for p in PROMPTS_DIR.glob("*.md")
                   if p.stem not in {"README", "CHANGELOG"})
    if "system" in names:
        names.remove("system")
        names.insert(0, "system")
    return names


def load(name: str = "system") -> Prompt:
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(
            f"No prompt named '{name}'. Available: {', '.join(available()) or '(none)'}"
        )

    raw = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.match(raw)

    if not match:
        # Frontmatter is optional. A bare markdown file is a valid prompt.
        return Prompt(name=name, text=raw.strip(), meta={})

    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"Frontmatter in {path.name} must be a mapping, got {type(meta)}.")

    return Prompt(name=name, text=match.group(2).strip(), meta=meta)
