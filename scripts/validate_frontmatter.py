"""Validate front matter on every Markdown page under docs/.

Usage: python scripts/validate_frontmatter.py [docs_dir]
Exits 1 if any page fails the schema in HANDBOOK-SPEC.md section 4.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

PAGE_TYPES = {
    "landing", "economics", "strategy", "kpi", "source-system", "data-domain",
    "dataset", "platform", "setup-guide",
    "access", "model-family", "feature", "causal-map", "lesson", "convention",
    "practice", "how-to", "how-we-work", "onboarding-path", "decision-record",
    "glossary", "app-registry",
}
AUDIENCES = {"ds", "mle", "de", "analyst", "product", "leadership", "all"}
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class FrontMatter(BaseModel):
    """Schema for a page's front matter."""

    model_config = ConfigDict(extra="forbid")

    title: str
    type: str
    owner: str
    audience: list[str]
    status: Literal["draft", "active", "deprecated"]
    last_reviewed: dt.date
    review_cadence: Literal["30d", "90d", "180d", "365d"]
    tags: list[str] = []
    sources: list[str] = []

    @field_validator("type")
    @classmethod
    def _type_known(cls, v: str) -> str:
        if v not in PAGE_TYPES:
            raise ValueError(f"unknown page type {v!r}")
        return v

    @field_validator("audience")
    @classmethod
    def _audience_known(cls, v: list[str]) -> list[str]:
        bad = sorted(set(v) - AUDIENCES)
        if not v or bad:
            raise ValueError(f"audience must be non-empty and within {sorted(AUDIENCES)}; bad: {bad}")
        return v

    @field_validator("tags")
    @classmethod
    def _tags_kebab(cls, v: list[str]) -> list[str]:
        bad = [t for t in v if not TAG_RE.match(t)]
        if bad:
            raise ValueError(f"tags must be lowercase kebab-case: {bad}")
        return v


def split_front_matter(text: str) -> dict | None:
    """Return the parsed front matter mapping, or None if the page has none."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return yaml.safe_load(text[4:end]) or {}


def validate(docs_dir: Path) -> list[str]:
    """Validate every page and return a list of error strings."""
    errors: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        data = split_front_matter(path.read_text(encoding="utf-8"))
        if data is None:
            errors.append(f"{path}: missing front matter")
            continue
        try:
            FrontMatter.model_validate(data)
        except ValidationError as exc:
            for err in exc.errors():
                loc = ".".join(str(x) for x in err["loc"]) or "front matter"
                errors.append(f"{path}: {loc}: {err['msg']}")
    return errors


def main() -> int:
    docs_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    errors = validate(docs_dir)
    for e in errors:
        print(e)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} error(s) across {sum(1 for _ in docs_dir.rglob('*.md'))} page(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
