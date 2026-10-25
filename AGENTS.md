# Agent contract

Instructions for any automated assistant (and a useful checklist for people)
editing this repository. The full rules are in `HANDBOOK-SPEC.md`; this file is
the short version you must follow.

## What this repository is

A team handbook: Markdown under `docs/`, facts under `facts/`, rendered to a
static site with Zensical. Pages describe how the business works, the
technology the team runs on, modeling knowledge, conventions, and how the team
operates.

## Rules

1. **Never invent a fact.** If a number, name, URL, quota, owner, or date is not
   in `facts/*.yaml`, in the page's listed `sources`, or in the request you were
   given, do not write it. Write `*[unverified: needs source]*` in its place and
   say so in your summary.
2. **Facts go in YAML, not prose.** Anything that can change (a KPI level, a
   quota, a team role, an app URL) is added to the right file under `facts/` and
   referenced in the page with a macro, for example
   `{{ kpis.items.<key>.current }}`. Do not type the value into the Markdown.
3. **Every page has a type.** Pick one from `HANDBOOK-SPEC.md` section 5, copy
   its template from `templates/`, and keep the required sections in order.
   If no type fits, stop and propose a spec change instead of improvising.
4. **Front matter is complete and valid.** Run
   `uv run --group docs python scripts/validate_frontmatter.py` before you
   finish. Fix every error.
5. **Do not bump `last_reviewed` yourself.** Only a person who has confirmed the
   content is correct changes that date. Formatting, link fixes, and moving
   facts into YAML do not count as a review.
6. **Use only the allowed Markdown** (spec section 6): CommonMark, tables,
   footnotes, definition lists, admonitions, content tabs, fenced code,
   Mermaid, snippets, and facts macros. No inline HTML. No renderer-specific
   syntax beyond these.
7. **Link, do not repeat.** If another page already explains something, link to
   it with a relative path. One topic per page.
8. **Decision records are append-only.** Never edit an accepted `DR-` file
   except to change its `Status` line.
9. **Blameless.** Lessons and decision records name causes and systems, never
   individuals as the cause.
10. **Build before you finish.** `uv run --group docs zensical build` must
    succeed with no warnings you introduced.

## Where things are

| Need | Location |
|---|---|
| Page type definitions and required sections | `HANDBOOK-SPEC.md` section 5 |
| Front matter schema | `HANDBOOK-SPEC.md` section 4 |
| Page templates | `templates/<type>.md` |
| Facts | `facts/kpis.yaml`, `facts/platform.yaml`, `facts/team.yaml`, `facts/apps.yaml` |
| Shared fragments | `includes/` |
| Site config and navigation | `zensical.toml` |
| Checks | `scripts/validate_frontmatter.py`, `scripts/stale_report.py` |

## Adding a page, in order

1. Choose the type. Copy `templates/<type>.md` to the right section directory.
2. Fill the front matter. `status: draft` until an owner reviews it.
3. Write the required sections. Move any changeable value into `facts/`.
4. Add the page to `nav` in `zensical.toml` and to its section `index.md`.
5. Run the validator and the build.
6. In your summary, list every `unverified` marker you left behind.
