"""Promote one release from the dev repositories to the release repositories.

Copies the exact bytes CI tested; nothing is rebuilt. Uses the Artifactory REST
API with the token from artifactory-auth.sh.
"""

import json
import os
import sys
import urllib.request

ARTIFACTORY = os.environ["ARTIFACTORY_URL"].rstrip("/") + "/artifactory"
TOKEN = os.environ["ARTIFACTORY_TOKEN"]


def call(method: str, path: str, body: dict | None = None) -> None:
    request = urllib.request.Request(
        f"{ARTIFACTORY}{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        print(method, path, response.status)


def main(package: str, version: str) -> None:
    env = os.environ
    # Python package files, stored by Artifactory as <package>/<version>/.
    call(
        "POST",
        f"/api/copy/{env['PYPI_DEV_LOCAL']}/{package}/{version}"
        f"?to=/{env['PYPI_RELEASE_LOCAL']}/{package}/{version}",
    )
    # Container image, same tag.
    call(
        "POST",
        f"/api/docker/{env['DOCKER_DEV_LOCAL']}/v2/promote",
        {
            "targetRepo": env["DOCKER_RELEASE_LOCAL"],
            "dockerRepository": package,
            "tag": version,
            "copy": True,
        },
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
