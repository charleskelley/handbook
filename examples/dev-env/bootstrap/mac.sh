#!/bin/bash
# Set up a Mac for local development with no Homebrew and no direct access to
# GitHub or PyPI: everything comes from Artifactory.
#
#   ARTIFACTORY_URL=https://artifactory.example.com bash mac.sh
#
# Installs uv, Python, a few CLI tools, and the Google Cloud CLI into your home
# directory. Run it again at any time to update. Needs no administrator rights.
set -euo pipefail

: "${ARTIFACTORY_URL:?Set ARTIFACTORY_URL, for example https://artifactory.example.com}"
UV_VERSION="${UV_VERSION:-0.9.0}"
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
RELEASES="${ARTIFACTORY_URL}/artifactory/github-releases"
host="${ARTIFACTORY_URL#https://}"
host="${host%%/*}"
bin="$HOME/.local/bin"
mkdir -p "$bin" "$HOME/.config/uv"

# 1. Credentials. Generate an identity token in the Artifactory web UI (Edit
#    Profile), paste it here. It is stored in ~/.netrc, readable by you only.
if ! grep -qs "machine $host" "$HOME/.netrc"; then
  read -r -p "Artifactory username: " user
  read -r -s -p "Artifactory identity token: " token
  echo
  umask 077
  printf 'machine %s login %s password %s\n' "$host" "$user" "$token" >> "$HOME/.netrc"
fi

# 2. uv, from Artifactory's cache of GitHub releases.
curl -fsSL --netrc \
  "$RELEASES/astral-sh/uv/releases/download/$UV_VERSION/uv-aarch64-apple-darwin.tar.gz" \
  | tar -xz --strip-components=1 -C "$bin"

# 3. uv points at Artifactory for packages and for Python itself.
cat > "$HOME/.config/uv/uv.toml" <<UV
python-install-mirror = "$RELEASES/astral-sh/python-build-standalone/releases/download"

[[index]]
name = "artifactory"
url = "$ARTIFACTORY_URL/artifactory/api/pypi/pypi/simple"
default = true
UV

# 4. Python and command line tools, all from Artifactory.
"$bin/uv" python install "$PYTHON_VERSION"
for tool in rust-just ruff pre-commit nbstripout; do
  "$bin/uv" tool install --upgrade "$tool"
done

# 5. Google Cloud CLI, from Artifactory's cache of dl.google.com.
if [ ! -x "$HOME/google-cloud-sdk/bin/gcloud" ]; then
  curl -fsSL --netrc \
    "$ARTIFACTORY_URL/artifactory/google-cloud-sdk/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz" \
    | tar -xz -C "$HOME"
  "$HOME/google-cloud-sdk/install.sh" --quiet --path-update=true --usage-reporting=false
fi

# 6. PATH for new shells.
profile="$HOME/.zprofile"
grep -qs '.local/bin' "$profile" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile"

echo "Done. Open a new terminal, then: gcloud auth login && gcloud auth application-default login"
