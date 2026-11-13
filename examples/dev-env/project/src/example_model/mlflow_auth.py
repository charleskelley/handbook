"""Sends a Google identity token with every MLflow request.

The tracking server is a Cloud Run service that requires IAM authentication. A
service account (CI, the pipeline) gets a token for the service URL; a person on
a workstation or laptop gets one from gcloud. Registered as an MLflow plugin in
pyproject.toml, so nothing calls this directly.
"""

from __future__ import annotations

import os
import subprocess
import time

from mlflow.tracking.request_header_provider import RequestHeaderProvider


class CloudRunHeaderProvider(RequestHeaderProvider):
    _token: str | None = None
    _expires: float = 0.0

    def in_context(self) -> bool:
        uri = os.environ.get("MLFLOW_TRACKING_URI") or os.environ.get(
            "EXAMPLE_MODEL_TRACKING_URI", ""
        )
        return uri.startswith("https://") and os.environ.get("EXAMPLE_MODEL_TRACKING_AUTH") != "off"

    def request_headers(self) -> dict[str, str]:
        if time.time() > self._expires:
            type(self)._token = _identity_token(os.environ.get("MLFLOW_TRACKING_URI", ""))
            type(self)._expires = time.time() + 45 * 60
        return {"Authorization": f"Bearer {self._token}"}


def _identity_token(audience: str) -> str:
    try:
        import google.auth.transport.requests
        import google.oauth2.id_token

        return google.oauth2.id_token.fetch_id_token(
            google.auth.transport.requests.Request(), audience
        )
    except Exception:
        # A person: fetch_id_token needs a service account; gcloud mints user tokens.
        return subprocess.run(
            ["gcloud", "auth", "print-identity-token"], capture_output=True, text=True, check=True
        ).stdout.strip()
