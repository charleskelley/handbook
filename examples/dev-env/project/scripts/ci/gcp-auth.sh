#!/bin/sh
# Authenticate to Google Cloud with workload identity federation: Google exchanges
# the job's GitLab OIDC token for short-lived credentials. No key files.
# Source this script: it exports GOOGLE_APPLICATION_CREDENTIALS.
set -eu

dir="${CI_BUILDS_DIR:-/tmp}"
printf '%s' "$GCP_OIDC_TOKEN" > "$dir/.gcp_oidc_token"
cat > "$dir/.gcp_credentials.json" <<JSON
{
  "type": "external_account",
  "audience": "//iam.googleapis.com/${GCP_WIF_PROVIDER}",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "token_url": "https://sts.googleapis.com/v1/token",
  "credential_source": {"file": "$dir/.gcp_oidc_token"},
  "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken"
}
JSON
export GOOGLE_APPLICATION_CREDENTIALS="$dir/.gcp_credentials.json"
if command -v gcloud >/dev/null 2>&1; then
  gcloud auth login --cred-file="$GOOGLE_APPLICATION_CREDENTIALS" --quiet
fi
