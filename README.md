# Handbook

A template for a data science and machine learning team's internal handbook:
how the business makes money and what it measures, the technology the team
runs on, the methods it uses and what it has learned using them, and how the
team works. Markdown in git, rendered to a static site, built so
that people and automated assistants can keep it current.

This repository is the empty, employer-neutral shape. Fork it inside your
company and fill it in.

## Run it

```sh
uv sync --group docs
uv run --group docs zensical serve      # http://localhost:8000
uv run --group docs zensical build      # writes site/
```

## Checks

```sh
uv run --group docs python scripts/validate_frontmatter.py   # schema, exits 1 on error
uv run --group docs python scripts/stale_report.py           # pages past review cadence
uv run --group docs pymarkdown scan docs/                    # Markdown lint
```

CI runs the same checks plus a link check on every pull request.

With [just](https://just.systems) installed, `just` lists shortcuts for all of
these: `just serve`, `just build`, `just check` (validate, lint, build, as CI
does), `just stale`, and `just clean`.

## The content contract

Three documents define how this handbook is written:

- **[`HANDBOOK-SPEC.md`](HANDBOOK-SPEC.md)**: sections, page types with their
  required headings, the front matter schema, the allowed Markdown subset, and
  how facts are kept out of prose.
- **[`AGENTS.md`](AGENTS.md)**: the short rule set an automated assistant (or a
  new contributor) follows when adding or editing a page.
- **`templates/`**: one Markdown template per strict page type. Copy, fill, link.
  Pages that fit no strict type are `general` and have no template.

Anything that changes (a KPI level, a quota, a URL, who owns what) lives in
`facts/*.yaml` and is rendered into pages with macros, so a number appears once
in the repository.

## Layout

```
docs/            the pages, one directory per section
facts/           YAML facts rendered into pages
includes/        shared Markdown fragments (snippets)
templates/       one template per page type
scripts/         validator, staleness report, notebook conversion
zensical.toml    site configuration and navigation
zoo/             untracked local working files (gitignored)
```

## Renderer

Built on [Zensical](https://zensical.org), the successor to Material for
MkDocs, pinned in `pyproject.toml`. Pages use only the Markdown subset in the
spec, so the renderer can be swapped; the configuration is also readable by
MkDocs with the Material theme as a fallback. Notebook pages are converted to
Markdown with `scripts/nb2md.sh` before the build rather than rendered live.

To use the alternate palette (green primary, gold accent), swap the commented
palette block in `zensical.toml`.

## License

Configuration, scripts, and templates: [Apache 2.0](LICENSE). Handbook prose
and the specification: [CC BY 4.0](LICENSE-CC-BY).
