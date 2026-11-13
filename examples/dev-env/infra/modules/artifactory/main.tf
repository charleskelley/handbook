# Every inbound dependency comes through these repositories, and every
# production artifact is promoted from a dev local repository to a release one.
#
#   <type>-dev-local      CI publishes every release candidate here
#   <type>-release-local  promotion copies tested candidates here
#   <type>-remote         caches of public sources
#   <type>                virtual: release + remotes. Developers and production
#   <type>-dev            virtual: dev + release + remotes. CI verify jobs only
#
# Python and Docker are wired. Add npm, Cargo, Go, Maven, Conan, and Debian
# repositories in the same shape when the first project needs them.

# ---- Python

resource "artifactory_local_pypi_repository" "dev" {
  key = "pypi-dev-local"
}

resource "artifactory_local_pypi_repository" "release" {
  key = "pypi-release-local"
}

resource "artifactory_remote_pypi_repository" "pypi" {
  key               = "pypi-remote"
  url               = "https://files.pythonhosted.org"
  pypi_registry_url = "https://pypi.org"
}

resource "artifactory_virtual_pypi_repository" "release" {
  key          = "pypi"
  repositories = [artifactory_local_pypi_repository.release.key, artifactory_remote_pypi_repository.pypi.key]
}

resource "artifactory_virtual_pypi_repository" "dev" {
  key = "pypi-dev"
  repositories = [
    artifactory_local_pypi_repository.dev.key,
    artifactory_local_pypi_repository.release.key,
    artifactory_remote_pypi_repository.pypi.key,
  ]
}

# ---- Docker

resource "artifactory_local_docker_v2_repository" "dev" {
  key = "docker-dev-local"
}

resource "artifactory_local_docker_v2_repository" "release" {
  key = "docker-release-local"
}

resource "artifactory_remote_docker_repository" "remotes" {
  for_each = {
    dockerhub-remote  = "https://registry-1.docker.io/"
    ghcr-remote       = "https://ghcr.io/"
    gcr-remote        = "https://gcr.io/"
    gcp-docker-remote = "https://${var.gcp_region}-docker.pkg.dev/"
  }
  key = each.key
  url = each.value
}

resource "artifactory_virtual_docker_repository" "release" {
  key = "docker"
  repositories = concat(
    [artifactory_local_docker_v2_repository.release.key],
    [for r in artifactory_remote_docker_repository.remotes : r.key],
  )
}

resource "artifactory_virtual_docker_repository" "dev" {
  key = "docker-dev"
  repositories = concat(
    [artifactory_local_docker_v2_repository.dev.key, artifactory_local_docker_v2_repository.release.key],
    [for r in artifactory_remote_docker_repository.remotes : r.key],
  )
}

# ---- Toolchains, SDKs, and models

# uv and python-build-standalone release assets, through
# <artifactory>/artifactory/github-releases/<owner>/<repo>/releases/download/...
resource "artifactory_remote_generic_repository" "github_releases" {
  key = "github-releases"
  url = "https://github.com"
}

# The Google Cloud CLI archive for laptops.
resource "artifactory_remote_generic_repository" "google_cloud_sdk" {
  key = "google-cloud-sdk"
  url = "https://dl.google.com"
}

# Terraform for the people who edit infrastructure.
resource "artifactory_remote_generic_repository" "hashicorp" {
  key = "hashicorp-releases"
  url = "https://releases.hashicorp.com"
}

# JetBrains Toolbox Agent and IDE backends for the workstation image, through
# <artifactory>/artifactory/jetbrains/toolbox/agent/... and .../python/...
resource "artifactory_remote_generic_repository" "jetbrains" {
  key = "jetbrains"
  url = "https://download.jetbrains.com"
}

# Pretrained models: set HF_ENDPOINT to <artifactory>/artifactory/api/huggingfaceml/huggingface
resource "artifactory_remote_huggingfaceml_repository" "huggingface" {
  key = "huggingface"
  url = "https://huggingface.co"
}
