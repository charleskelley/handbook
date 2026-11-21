# Handbook tasks. Run `just` to list them.

docs := "uv run --group docs"

# List the recipes
default:
    @just --list

# Serve the site with live reload at http://localhost:8000
serve addr="localhost:8000":
    {{docs}} zensical serve --dev-addr {{addr}}

# Serve and open the site in the default browser
open addr="localhost:8000":
    {{docs}} zensical serve --dev-addr {{addr}} --open

# Build the site into site/
build:
    {{docs}} zensical build

# Build from a clean cache
rebuild:
    {{docs}} zensical build --clean

# Validate front matter, required headings, and fact links
validate:
    {{docs}} python scripts/validate_frontmatter.py docs

# Lint the Markdown
lint:
    {{docs}} pymarkdown --config .pymarkdown.json scan -r docs

# List pages past their review cadence
stale:
    {{docs}} python scripts/stale_report.py docs

# Regenerate the generated diagrams (docs/assets/)
diagram:
    {{docs}} --with pillow python scripts/dpom_diagram.py
    {{docs}} python scripts/customer_base_audit_diagram.py
    {{docs}} python scripts/rfm_diagram.py
    {{docs}} python scripts/method_diagrams.py

# Run the same checks as CI: validate, lint, build
check: validate lint build

# Remove the built site and the cache
clean:
    rm -rf site .cache
