#!/bin/bash
# Cloud Workstations runs /etc/workstation-startup.d/* as root at every start.
# Reads the read-only Artifactory token with the workstation's service account
# and writes it to the user's ~/.netrc, where uv, pip, and curl find it.
# ARTIFACTORY_URL, ARTIFACTORY_USER, and ARTIFACTORY_TOKEN_SECRET come from the
# workstation configuration's container environment (Terraform).
set -euo pipefail

user_home=/home/user
host="${ARTIFACTORY_URL#https://}"
host="${host%%/*}"
token="$(gcloud secrets versions access latest --secret="${ARTIFACTORY_TOKEN_SECRET}")"

umask 077
printf 'machine %s login %s password %s\n' "$host" "$ARTIFACTORY_USER" "$token" > "$user_home/.netrc"
chown user:user "$user_home/.netrc"

profile=/etc/profile.d/artifactory.sh
echo "export HF_ENDPOINT=${ARTIFACTORY_URL}/artifactory/api/huggingfaceml/huggingface" > "$profile"
