# Cloud Run, Vertex AI, and Cloud Workstations pull images from Artifact
# Registry. This remote repository is a pull-through cache of Artifactory, so
# Artifactory stays the only source. An image at
#   <artifactory-host>/<artifactory-repo>/<image>:<tag>
# is pulled by Google services as
#   <region>-docker.pkg.dev/<project>/<repository_id>/<artifactory-repo>/<image>:<tag>
# The credentials decide what the mirror can see: production uses a token that
# reads the release repository only.

resource "google_artifact_registry_repository" "mirror" {
  project       = var.project
  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
  mode          = "REMOTE_REPOSITORY"
  description   = "Pull-through cache of Artifactory"

  remote_repository_config {
    description = "Artifactory"
    docker_repository {
      custom_repository {
        uri = var.artifactory_url
      }
    }
    upstream_credentials {
      username_password_credentials {
        username                = var.username
        password_secret_version = var.password_secret_version
      }
    }
  }
}

data "google_project" "this" {
  project_id = var.project
}

# Artifact Registry reads the Artifactory token from Secret Manager.
resource "google_secret_manager_secret_iam_member" "registry_agent" {
  project   = var.project
  secret_id = var.password_secret
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:service-${data.google_project.this.number}@gcp-sa-artifactregistry.iam.gserviceaccount.com"
}

resource "google_artifact_registry_repository_iam_member" "readers" {
  for_each   = toset(var.readers)
  project    = var.project
  location   = var.region
  repository = google_artifact_registry_repository.mirror.repository_id
  role       = "roles/artifactregistry.reader"
  member     = each.value
}
