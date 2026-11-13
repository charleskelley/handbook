# The team MLflow tracking server: Cloud Run in front of Cloud SQL Postgres and
# a GCS artifact bucket, following MLflow's own GCP recipe. The service requires
# IAM authentication: people and service accounts send a Google identity token,
# which the project's MLflow plugin does for them. Scales to zero; the database
# is the only always-on cost.

resource "google_service_account" "server" {
  project      = var.project
  account_id   = "mlflow-server"
  display_name = "MLflow tracking server"
}

# ---- Backend store

resource "google_sql_database_instance" "mlflow" {
  project             = var.project
  name                = "mlflow"
  region              = var.region
  database_version    = "POSTGRES_16"
  deletion_protection = true

  settings {
    tier              = var.database_tier
    availability_type = "ZONAL"
    disk_autoresize   = true
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }
    ip_configuration {
      ipv4_enabled = false
      private_network = var.network
    }
  }
}

resource "google_sql_database" "mlflow" {
  project  = var.project
  instance = google_sql_database_instance.mlflow.name
  name     = "mlflow"
}

resource "random_password" "db" {
  length  = 32
  special = false
}

resource "google_sql_user" "mlflow" {
  project  = var.project
  instance = google_sql_database_instance.mlflow.name
  name     = "mlflow"
  password = random_password.db.result
}

# The connection string is a secret: it carries the password.
resource "google_secret_manager_secret" "backend_uri" {
  project   = var.project
  secret_id = "mlflow-backend-store-uri"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "backend_uri" {
  secret = google_secret_manager_secret.backend_uri.id
  secret_data = join("", [
    "postgresql+psycopg2://mlflow:${random_password.db.result}@/mlflow",
    "?host=/cloudsql/${google_sql_database_instance.mlflow.connection_name}",
  ])
}

resource "google_secret_manager_secret_iam_member" "server_reads_uri" {
  project   = var.project
  secret_id = google_secret_manager_secret.backend_uri.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = google_service_account.server.member
}

resource "google_project_iam_member" "server_sql_client" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = google_service_account.server.member
}

# ---- Artifact store. Served through the tracking server (--serve-artifacts),
# so clients need no bucket access of their own.

resource "google_storage_bucket" "artifacts" {
  project                     = var.project
  name                        = var.artifact_bucket
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  versioning {
    enabled = false
  }
}

resource "google_storage_bucket_iam_member" "server_writes_artifacts" {
  bucket = google_storage_bucket.artifacts.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.server.member
}

# ---- The service

resource "google_cloud_run_v2_service" "mlflow" {
  project  = var.project
  name     = "mlflow"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account                  = google_service_account.server.email
    max_instance_request_concurrency = 80
    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }
    containers {
      image = var.image
      ports {
        container_port = 8080
      }
      env {
        name = "MLFLOW_BACKEND_STORE_URI"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.backend_uri.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "MLFLOW_ARTIFACTS_DESTINATION"
        value = "gs://${google_storage_bucket.artifacts.name}/artifacts"
      }
      resources {
        limits = { cpu = "1", memory = "1Gi" }
      }
      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.mlflow.connection_name]
      }
    }
  }

  depends_on = [google_secret_manager_secret_version.backend_uri]
}

# No unauthenticated access: every caller presents an identity token.
resource "google_cloud_run_v2_service_iam_member" "invokers" {
  for_each = toset(var.invokers)
  project  = var.project
  location = var.region
  name     = google_cloud_run_v2_service.mlflow.name
  role     = "roles/run.invoker"
  member   = each.value
}
