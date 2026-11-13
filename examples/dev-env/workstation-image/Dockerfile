# The team workstation image. CI builds it from Google's Code OSS base image,
# pulled through Artifactory, and Cloud Workstations pulls the result through the
# Artifact Registry mirror. Rebuilt, never patched in place: changes go here.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG ARTIFACTORY_URL
ARG UV_VERSION
# The Toolbox App on every laptop must be this exact build (its About tab).
ARG JETBRAINS_TOOLBOX_BUILD
# Path of the PyCharm Linux archive under download.jetbrains.com, for example
# python/pycharm-<version>.tar.gz. Read it from the JetBrains releases API.
ARG PYCHARM_ARCHIVE

# uv from Artifactory's cache of GitHub releases.
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    curl -fsSL --netrc \
      "${ARTIFACTORY_URL}/artifactory/github-releases/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" \
    | tar -xz --strip-components=1 -C /usr/local/bin

# uv for every user: Artifactory as the only index and the Python mirror.
RUN mkdir -p /etc/uv && printf '%s\n' \
      "python-install-mirror = \"${ARTIFACTORY_URL}/artifactory/github-releases/astral-sh/python-build-standalone/releases/download\"" \
      "" \
      "[[index]]" \
      "name = \"artifactory\"" \
      "url = \"${ARTIFACTORY_URL}/artifactory/api/pypi/pypi/simple\"" \
      "default = true" \
    > /etc/uv/uv.toml

# JetBrains remote development, fully offline: the Toolbox Agent that the
# Toolbox App would otherwise push to the host, and the PyCharm backend it would
# otherwise download. Both come from Artifactory's cache of download.jetbrains.com.
# The Agent build must match the Toolbox App build on the laptop exactly.
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    mkdir -p /opt/jetbrains/tbcli /opt/jetbrains/pycharm \
    && curl -fsSL --netrc \
      "${ARTIFACTORY_URL}/artifactory/jetbrains/toolbox/agent/tbcli-linux-x64-${JETBRAINS_TOOLBOX_BUILD}.tar.gz" \
    | tar -xz -C /opt/jetbrains/tbcli \
    && curl -fsSL --netrc "${ARTIFACTORY_URL}/artifactory/jetbrains/${PYCHARM_ARCHIVE}" \
    | tar -xz --strip-components=1 -C /opt/jetbrains/pycharm \
    && mkdir -p /etc/xdg/JetBrains/ToolboxSshDeploy \
    && echo "cli_dir_path=/opt/jetbrains/tbcli" > /etc/xdg/JetBrains/ToolboxSshDeploy/env.sh

# Run at every workstation start: Artifactory credentials, then the JetBrains
# registration of the preinstalled backend in the user's home.
COPY 200_artifactory.sh 210_jetbrains.sh /etc/workstation-startup.d/
RUN chmod 0755 /etc/workstation-startup.d/200_artifactory.sh /etc/workstation-startup.d/210_jetbrains.sh
