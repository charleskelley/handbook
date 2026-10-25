#!/usr/bin/env sh
# Convert a Jupyter notebook to a Markdown page with extracted images.
# Usage: scripts/nb2md.sh path/to/notebook.ipynb docs/modeling/notebooks
# Requires nbconvert: uv add --group notebooks nbconvert
# The output page still needs front matter added by hand (see templates/).
set -eu
nb="$1"; out="${2:-docs/modeling/notebooks}"
mkdir -p "$out"
uv run --group notebooks jupyter nbconvert --to markdown "$nb" --output-dir "$out"
echo "Wrote $out/$(basename "${nb%.ipynb}").md. Add front matter before committing."
