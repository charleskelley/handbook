"""Validate pages, templates, and fact links against HANDBOOK-SPEC.md.

Usage: python scripts/validate_frontmatter.py [docs_dir]
Checks front matter (section 4), required headings on strict pages and templates
(section 5), that no wireframe prompt remains on an active page (section 6),
and links held in facts (section 7). Exits 1 on any error. Pages that
use a placeholder `example` fact key print a warning and do not fail.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

# Required H2 headings per strict type, in order. Mirrors HANDBOOK-SPEC.md section 5.
REQUIRED_HEADINGS: dict[str, list[str]] = {
    "business-overview": [
        "What the company does", "Products and segments", "How money is made",
        "Customers and markets", "Operations", "Regulation and risk",
        "Seasonality and cycles", "Organization", "What this means for the team",
    ],
    "decision-inventory": [
        "How to read this page", "Decisions", "Candidates for an outcome loop",
        "How a row changes",
    ],
    "kpi": [
        "Definition", "Formula", "Current level", "Owner and source of truth",
        "What moves it", "Common misreadings", "Related KPIs",
    ],
    "source-system": [
        "What it is", "System of record for", "What it emits", "How it lands",
        "Owner and contact",
    ],
    "data-domain": [
        "Scope", "Model", "Canonical tables", "How to join", "Conventions", "Owner",
    ],
    "dataset": [
        "What it holds", "Where it comes from", "Freshness and retention",
        "Columns that matter", "Quality checks", "Known issues", "Used by",
    ],
    "method": [
        "What it is", "When it is the right choice", "When it is not",
        "Where it applies to our data", "Lessons learned", "Reference implementations",
    ],  # the sections every method page has; depth and the causal tag add more
    "platform": [
        "What it is for", "Architecture", "How we use it", "Limits and quotas",
        "Owner and support path", "Runbooks",
    ],
    "how-to": ["Goal", "Steps", "Verify", "See also"],
    "decision-record": [
        "Context", "Decision", "Alternatives considered", "Consequences", "Status",
    ],
    "insight": [
        "What is true", "When it applied", "How we know", "What it affects",
        "Does it still hold",
    ],
}
# A method page's depth adds sections, and so does the `causal` tag. Each entry is
# (heading, the required heading it goes before, or None for the end).
METHOD_DEPTH_HEADINGS: dict[str, list[tuple[str, str | None]]] = {
    "build": [
        ("Building the outputs", "Where it applies to our data"),
        ("Checks", "Where it applies to our data"),
        ("Pitfalls", "Where it applies to our data"),
        ("Worked examples", "Where it applies to our data"),
    ],
    "guide": [
        ("Common approaches", "Where it applies to our data"),
        ("Reading a result you did not produce", "Where it applies to our data"),
        ("Further reading", None),
    ],
}
METHOD_CAUSAL_HEADING = ("Assumptions", "Where it applies to our data")
METHOD_CAUSAL_AFTER = "When it is not"
# A source-system page that is a system directory's index also maps its contents.
SYSTEM_INDEX_HEADING = "What's here"
PAGE_TYPES = {*REQUIRED_HEADINGS, "general"}
AUDIENCES = {"ds", "mle", "de", "analyst", "product", "leadership", "all"}
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
H2_RE = re.compile(r"^## +(.+?)(?: *\{[^}]*\})? *$")
ANCHOR_RE = re.compile(r"\{: *#([A-Za-z0-9_-]+)[^}]*\}")
EXAMPLE_KEY_RE = re.compile(r"\{[{%][^}]*\bexample\b")
# A wireframe prompt (spec section 6). None may remain on an active page.
ADD_PROMPT_RE = re.compile(r"\*Add:")


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
    depth: Literal["build", "guide"] | None = None

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


def body_of(text: str) -> str:
    """Return the page text after its front matter."""
    end = text.find("\n---\n", 4)
    return text[end + 5:] if text.startswith("---\n") and end != -1 else text


def h2_headings(text: str) -> list[str]:
    """Return the H2 headings of a page, ignoring fenced code."""
    headings: list[str] = []
    fenced = False
    for line in body_of(text).splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and (match := H2_RE.match(line)):
            headings.append(match.group(1))
    return headings


def method_headings(depth: str | None, causal: bool) -> list[str]:
    """Return the required headings of a method page of this depth, in order."""
    required = list(REQUIRED_HEADINGS["method"])
    if causal:
        required.insert(required.index(METHOD_CAUSAL_AFTER) + 1, METHOD_CAUSAL_HEADING[0])
    for name, before in METHOD_DEPTH_HEADINGS.get(depth or "", []):
        required.insert(required.index(before) if before else len(required), name)
    return required


def heading_errors(
    page_type: str, text: str, is_system_index: bool = False,
    depth: str | None = None, causal: bool = False,
) -> list[str]:
    """Return problems with a page's required headings, missing or out of order."""
    required = list(REQUIRED_HEADINGS.get(page_type, []))
    if page_type == "method":
        required = method_headings(depth, causal)
    if page_type == "source-system" and is_system_index:
        required.append(SYSTEM_INDEX_HEADING)
    found = h2_headings(text)
    errors = [f"missing required section {name!r}" for name in required if name not in found]
    if errors:
        return errors
    present = [name for name in found if name in required]
    if present != required:
        errors.append(f"required sections out of order: expected {required}")
    return errors


def validate(docs_dir: Path) -> list[str]:
    """Validate every page and return a list of error strings."""
    errors: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        data = split_front_matter(text)
        if data is None:
            errors.append(f"{path}: missing front matter")
            continue
        try:
            FrontMatter.model_validate(data)
        except ValidationError as exc:
            for err in exc.errors():
                loc = ".".join(str(x) for x in err["loc"]) or "front matter"
                errors.append(f"{path}: {loc}: {err['msg']}")
            continue
        is_system_index = path.name == "index.md" and path.parent.parent == docs_dir / "data" / "sources"
        depth, is_method = data.get("depth"), data["type"] == "method"
        if is_method != (depth is not None):
            errors.append(f"{path}: depth is required on a method page and allowed on no other")
        causal = "causal" in data.get("tags", [])
        errors += [
            f"{path}: {e}"
            for e in heading_errors(data["type"], text, is_system_index, depth, causal)
        ]
        if data["status"] == "active" and (n := len(ADD_PROMPT_RE.findall(body_of(text)))):
            errors.append(f"{path}: active page still has {n} wireframe prompt(s) (*Add:*)")
    return errors


def validate_templates(templates_dir: Path) -> list[str]:
    """Check that the templates are exactly the strict types, with their headings."""
    errors: list[str] = []
    found = {path.stem for path in templates_dir.glob("*.md")}
    errors += [f"{templates_dir}: no template for type {t!r}" for t in sorted(set(REQUIRED_HEADINGS) - found)]
    errors += [f"{templates_dir}: {t}.md matches no strict type" for t in sorted(found - set(REQUIRED_HEADINGS))]
    for page_type in sorted(found & set(REQUIRED_HEADINGS)):
        path = templates_dir / f"{page_type}.md"
        text = path.read_text(encoding="utf-8")
        # The method template carries the sections of both depths and of a causal page.
        depths = list(METHOD_DEPTH_HEADINGS) if page_type == "method" else [None]
        for depth in depths:
            errors += [
                f"{path}: {e}"
                for e in heading_errors(page_type, text, depth=depth, causal=page_type == "method")
            ]
    return errors


def link_error(docs_dir: Path, link: str) -> str | None:
    """Return why a docs-relative link with an optional anchor does not resolve."""
    target, _, anchor = link.partition("#")
    path = docs_dir / target
    if not path.is_file():
        return f"page {target!r} does not exist"
    if anchor and anchor not in ANCHOR_RE.findall(path.read_text(encoding="utf-8")):
        return f"anchor #{anchor} not found in {target}"
    return None


def validate_fact_links(docs_dir: Path, facts_dir: Path) -> list[str]:
    """Check links held in facts. Keys starting with `example` are placeholders."""
    errors: list[str] = []

    def load(name: str) -> dict:
        return yaml.safe_load((facts_dir / f"{name}.yaml").read_text(encoding="utf-8"))[name]

    def check(source: str, key: str, link: str | None) -> None:
        if link and not key.startswith("example") and (problem := link_error(docs_dir, link)):
            errors.append(f"{facts_dir}/{source}.yaml: {key}: {problem}")

    for key, item in load("kpis")["items"].items():
        check("kpis", key, item.get("page"))
    for key, item in load("data")["datasets"].items():
        check("data", key, item.get("page"))
    for key, item in load("team")["rituals"].items():
        check("team", key, item.get("page"))
    for key, item in load("apps")["items"].items():
        for link in item.get("linked_from") or []:
            check("apps", key, link)
    for category in load("insights")["categories"].values():
        for key, item in (category["items"] or {}).items():
            if item.get("kind") not in ("endogenous", "exogenous"):
                errors.append(f"{facts_dir}/insights.yaml: {key}: kind must be endogenous or exogenous")
            if not item.get("link"):
                errors.append(f"{facts_dir}/insights.yaml: {key}: link is required")
            check("insights", key, item.get("link"))
    return errors


def example_key_warnings(docs_dir: Path) -> list[str]:
    """Return pages that render a placeholder `example` fact."""
    return [
        f"warning: {path}: uses an example fact key"
        for path in sorted(docs_dir.rglob("*.md"))
        if EXAMPLE_KEY_RE.search(path.read_text(encoding="utf-8"))
    ]


def main() -> int:
    docs_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    root = docs_dir.resolve().parent
    errors = validate(docs_dir) + validate_templates(root / "templates") + validate_fact_links(docs_dir, root / "facts")
    for line in example_key_warnings(docs_dir) + errors:
        print(line)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} error(s) across {sum(1 for _ in docs_dir.rglob('*.md'))} page(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
