#!/bin/sh
# Exchange the job's GitLab OIDC token for a short-lived Artifactory access token
# and write it where uv, docker, and curl look for credentials. No stored secrets.
# Requires an OIDC integration named JFROG_OIDC_PROVIDER in the JFrog Platform.
# Source this script: it exports ARTIFACTORY_TOKEN and UV_PUBLISH_TOKEN.
set -eu

body="{\"grant_type\": \"urn:ietf:params:oauth:grant-type:token-exchange\", \"subject_token_type\": \"urn:ietf:params:oauth:token-type:id_token\", \"subject_token\": \"${JFROG_OIDC_TOKEN}\", \"provider_name\": \"${JFROG_OIDC_PROVIDER}\"}"
url="${ARTIFACTORY_URL}/access/api/v1/oidc/token"

if command -v python3 >/dev/null 2>&1; then
  ARTIFACTORY_TOKEN="$(BODY="$body" URL="$url" python3 -c '
import json, os, urllib.request
req = urllib.request.Request(os.environ["URL"], os.environ["BODY"].encode(), {"Content-Type": "application/json"})
print(json.load(urllib.request.urlopen(req))["access_token"])')"
else
  # Alpine-based images such as docker: busybox wget and sed.
  ARTIFACTORY_TOKEN="$(wget -qO- --header 'Content-Type: application/json' --post-data "$body" "$url" \
    | sed -n 's/.*"access_token" *: *"\([^"]*\)".*/\1/p')"
fi
export ARTIFACTORY_TOKEN
export UV_PUBLISH_TOKEN="$ARTIFACTORY_TOKEN"

host="${ARTIFACTORY_URL#https://}"
host="${host%%/*}"
umask 077
printf 'machine %s login %s password %s\n' "$host" "${ARTIFACTORY_USER:-gitlab}" "$ARTIFACTORY_TOKEN" > "$HOME/.netrc"
