# Agent contract

Instructions for any automated assistant (and a useful checklist for people)
editing this repository. The full rules are in `HANDBOOK-SPEC.md`; this file is
the short version you must follow.

## What this repository is

A team handbook: Markdown under `docs/`, facts under `facts/`, rendered to a
static site with Zensical. Pages describe how the business works, the
technology the team runs on, the methods it uses, and how the team operates.

## Rules

1. **Never invent a fact.** If a number, name, URL, quota, owner, or date is not
   in `facts/*.yaml`, in the page's listed `sources`, or in the request you were
   given, do not write it. Write `*[unverified: needs source]*` in its place and
   say so in your summary.
2. **Facts go in YAML, not prose.** Anything that can change (a KPI level, a
   quota, a team role, an app URL) is added to the right file under `facts/` and
   referenced in the page with a macro, for example
   `{{ kpis["items"].<key>.current }}`. Do not type the value into the Markdown.
3. **Every page has a type.** If a strict type from `HANDBOOK-SPEC.md` section 5
   fits, copy its template from `templates/` and keep the required sections in
   order. If none fits, use `type: general`, which has no required sections.
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
9. **Blameless.** Insights and decision records name causes and systems, never
   individuals as the cause.
10. **Build before you finish.** `uv run --group docs zensical build` must
    succeed with no warnings you introduced.

## Where things are

| Need | Location |
|---|---|
| Page type definitions and required sections | `HANDBOOK-SPEC.md` section 5 |
| Front matter schema | `HANDBOOK-SPEC.md` section 4 |
| Page templates | `templates/<type>.md` |
| Facts | `facts/kpis.yaml`, `facts/data.yaml`, `facts/platform.yaml`, `facts/team.yaml`, `facts/apps.yaml`, `facts/insights.yaml` |
| Shared fragments | `includes/` |
| Site config and navigation | `zensical.toml` |
| Checks | `scripts/validate_frontmatter.py`, `scripts/stale_report.py` |

## Which assistant for which page

The templates, the facts rule, and the validator make most pages a structured
fill-in task, so a small model is enough when the source material is in the
request and the checker runs in the loop. Judgment-heavy sections need a
larger model. Suggested split, by page type:

| Tier | Page types | Why |
|---|---|---|
| Small (Haiku-class) | dataset, source-system, data-domain, platform, how-to, decision-record from notes, section indexes, glossary, facts entries | Transcription from a schema dump, runbook, ticket, or notes into a fixed shape. Low judgment, high volume. |
| Mid (Sonnet-class) | kpi, method, insight, general pages such as business pages and how-we-work | Each has a section that weighs evidence or states what is not known. The default for anything a partner will read. |
| Large (Opus-class) | Spec changes, cross-page audits, restructuring, staleness reviews touching many owners | Multi-file reasoning where consistency across the handbook matters more than any one page. |

Three things matter more than the tier:

1. **Source material in the request.** The assistant's job is to transcribe and
   shape, not to know. A dataset page from a column listing and a pipeline
   config is a small-model task. A dataset page from nothing is a fabrication
   task at any size.
2. **The checker in the loop.** Run the validator and the build after every
   generation and feed the errors back.
3. **Owner review before `status: active`.** The assistant drafts, the owner
   reviews and bumps `last_reviewed`. That is the control, not the model.

Before trusting a tier for a page type, test it once: supply a real source with
two facts deliberately missing and check whether the output leaves two
`*[unverified: needs source]*` markers or writes two plausible values. If it
marks, it passes. If it invents, move that type up a tier.

## Adding a page, in order

1. Choose the type. Copy `templates/<type>.md` to the right section directory,
   or start from the front matter alone for a `general` page.
2. Fill the front matter. `status: draft` until an owner reviews it.
3. Write the required sections. Move any changeable value into `facts/`. Add any
   insight to `facts/insights.yaml`.
4. Add the page to `nav` in `zensical.toml` and to its section `index.md`.
5. Run the validator and the build.
6. In your summary, list every `unverified` marker you left behind.
