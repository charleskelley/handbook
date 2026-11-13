# The research notebook image for Vertex AI Workbench: Google's Workbench
# container plus the project's locked dependencies, so a notebook has the same
# package versions as the project. Built from the project directory:
#
#   docker build -f notebook-image/Dockerfile \
#     --build-arg BASE_IMAGE=<artifactory>/docker/deeplearning-platform-release/workbench-container:latest \
#     --build-arg UV_IMAGE=<artifactory>/docker/astral-sh/uv:0.9 \
#     --build-arg INDEX_URL=<artifactory>/artifactory/api/pypi/pypi/simple \
#     --secret id=netrc,src=$HOME/.netrc .
#
# The project itself is not installed. In a clone, install it in editable mode
# with no downloads, so notebooks import the package:
#   uv pip install --python python3 --no-deps --no-build-isolation -e .
ARG UV_IMAGE
ARG BASE_IMAGE
FROM ${UV_IMAGE} AS uv

FROM ${BASE_IMAGE}
ARG INDEX_URL
COPY --from=uv /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock /tmp/project/
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    uv export --project /tmp/project --frozen --all-extras --no-emit-project --no-hashes \
      -o /tmp/requirements.txt \
    && uv pip install --python "$(command -v python3)" --index-url "${INDEX_URL}" \
      -r /tmp/requirements.txt uv_build \
    && rm -rf /tmp/project /tmp/requirements.txt
