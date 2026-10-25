"""Report pages whose last_reviewed plus review_cadence is in the past.

Usage: python scripts/stale_report.py [docs_dir] [--fail]
Prints a table grouped by owner. With --fail, exits 1 if any page is stale.
"""

from __future__ import annotations

import datetime as dt
import sys
from collections import defaultdict
from pathlib import Path

from validate_frontmatter import split_front_matter

CADENCE_DAYS = {"30d": 30, "90d": 90, "180d": 180, "365d": 365}


def stale_pages(docs_dir: Path, today: dt.date) -> dict[str, list[tuple[Path, dt.date, int]]]:
    """Return stale pages grouped by owner as (path, due_date, days_overdue)."""
    out: dict[str, list[tuple[Path, dt.date, int]]] = defaultdict(list)
    for path in sorted(docs_dir.rglob("*.md")):
        fm = split_front_matter(path.read_text(encoding="utf-8")) or {}
        reviewed, cadence = fm.get("last_reviewed"), fm.get("review_cadence")
        if not isinstance(reviewed, dt.date) or cadence not in CADENCE_DAYS:
            continue
        if fm.get("status") == "deprecated":
            continue
        due = reviewed + dt.timedelta(days=CADENCE_DAYS[cadence])
        if due < today:
            out[str(fm.get("owner", "unowned"))].append((path, due, (today - due).days))
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    docs_dir = Path(args[0] if args else "docs")
    stale = stale_pages(docs_dir, dt.date.today())
    total = sum(len(v) for v in stale.values())
    if not total:
        print("No stale pages.")
        return 0
    print(f"{total} stale page(s)\n")
    for owner in sorted(stale):
        print(f"## {owner}")
        for path, due, overdue in sorted(stale[owner], key=lambda r: -r[2]):
            print(f"- {path}  due {due}  ({overdue} days overdue)")
        print()
    return 1 if "--fail" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
