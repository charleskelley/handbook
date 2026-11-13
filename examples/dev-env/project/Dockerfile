# The production image installs the *published* package from Artifactory, never
# the source tree, so the container runs exactly what CI tested and promoted.
#
#   docker build \
#     --build-arg BASE_IMAGE=<artifactory>/docker/python:3.12-slim \
#     --build-arg UV_IMAGE=<artifactory>/docker/astral-sh/uv:0.9 \
#     --build-arg INDEX_URL=<artifactory>/artifactory/api/pypi/pypi-dev/simple \
#     --build-arg PACKAGE_VERSION=0.1.0 \
#     --secret id=netrc,src=$HOME/.netrc .
ARG UV_IMAGE
ARG BASE_IMAGE
FROM ${UV_IMAGE} AS uv

FROM ${BASE_IMAGE}
ARG INDEX_URL
ARG PACKAGE_VERSION
COPY --from=uv /uv /usr/local/bin/uv
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    uv pip install --system --no-cache --index-url "${INDEX_URL}" \
      "example-model[gcp,serve,monitor]==${PACKAGE_VERSION}"
RUN useradd --uid 10001 --no-create-home app
USER app
ENV PORT=8080
# Cloud Run service: serve. Cloud Run jobs override the command: score,
# performance, report.
# Vertex AI Pipelines: the pipeline sets `example-model train ...`.
CMD ["example-model", "serve"]
