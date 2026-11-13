# The prod project: identities, the mirror that serves only released images,
# governed model storage, and the trust that lets GitLab release tags deploy.
# Cloud Run services and jobs and Vertex AI pipeline runs are created by the
# deploy and train jobs in CI, from released artifacts.

resource "google_service_account" "deployer" {
  account_id   = "deployer"
  display_name = "GitLab CI release jobs"
}

resource "google_service_account" "run" {
  account_id   = "example-model-run"
  display_name = "example-model on Cloud Run"
}

resource "google_service_account" "train" {
  account_id   = "example-model-train"
  display_name = "example-model training pipeline"
}

module "registry_mirror" {
  source                  = "../../modules/registry-mirror"
  project                 = var.project
  region                  = var.region
  artifactory_url         = var.artifactory_url
  username                = var.artifactory_release_user
  password_secret         = var.artifactory_token_secret
  password_secret_version = "projects/${var.project}/secrets/${var.artifactory_token_secret}/versions/latest"
  readers = [
    google_service_account.run.member,
    google_service_account.train.member,
    google_service_account.deployer.member,
  ]
}

# ---- Model and pipeline storage

resource "google_storage_bucket" "models" {
  name                        = var.models_bucket
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "pipelines" {
  name                        = var.pipelines_bucket
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

resource "google_storage_bucket_iam_member" "train_writes_models" {
  bucket = google_storage_bucket.models.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.train.member
}

resource "google_storage_bucket_iam_member" "run_reads_models" {
  bucket = google_storage_bucket.models.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.run.member
}

resource "google_storage_bucket_iam_member" "train_pipeline_root" {
  bucket = google_storage_bucket.pipelines.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.train.member
}

# ---- Monitoring: the prediction log, labels, metrics, reports, schedules, alerts

resource "google_bigquery_dataset" "monitoring" {
  dataset_id = "model_monitoring"
  location   = var.region
}

# Every batch prediction, appended by the score job. Partitioned by scored_at,
# which Vertex AI Model Monitoring uses as its timestamp field.
resource "google_bigquery_table" "predictions" {
  dataset_id          = google_bigquery_dataset.monitoring.dataset_id
  table_id            = "predictions"
  deletion_protection = true
  time_partitioning {
    type  = "DAY"
    field = "scored_at"
  }
  clustering = ["model_version"]
  schema = jsonencode([
    { name = "entity_id", type = "STRING", mode = "REQUIRED" },
    { name = "score", type = "FLOAT", mode = "REQUIRED" },
    { name = "model_version", type = "STRING", mode = "REQUIRED" },
    { name = "as_of", type = "STRING", mode = "NULLABLE" },
    { name = "scored_at", type = "TIMESTAMP", mode = "REQUIRED" },
    # Feature columns are added by the load job (schema update on append).
  ])
}

# The contract for labels: who, what, when. Filled by the business process that
# learns the outcome, days to months after the prediction.
resource "google_bigquery_table" "labels" {
  dataset_id          = google_bigquery_dataset.monitoring.dataset_id
  table_id            = "labels"
  deletion_protection = true
  time_partitioning {
    type  = "DAY"
    field = "labeled_at"
  }
  schema = jsonencode([
    { name = "entity_id", type = "STRING", mode = "REQUIRED" },
    { name = "label", type = "INTEGER", mode = "REQUIRED" },
    { name = "labeled_at", type = "TIMESTAMP", mode = "REQUIRED" },
  ])
}

resource "google_bigquery_table" "model_metrics" {
  dataset_id          = google_bigquery_dataset.monitoring.dataset_id
  table_id            = "model_metrics"
  deletion_protection = false
  schema = jsonencode([
    { name = "model_version", type = "STRING", mode = "REQUIRED" },
    { name = "week_start", type = "TIMESTAMP", mode = "REQUIRED" },
    { name = "n", type = "INTEGER", mode = "REQUIRED" },
    { name = "roc_auc", type = "FLOAT", mode = "REQUIRED" },
    { name = "average_precision", type = "FLOAT", mode = "REQUIRED" },
    { name = "computed_at", type = "TIMESTAMP", mode = "REQUIRED" },
  ])
}

# Evidently reports and Model Monitoring output. Static files, read by people.
resource "google_storage_bucket" "reports" {
  name                        = var.reports_bucket
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

resource "google_storage_bucket_iam_member" "run_writes_reports" {
  bucket = google_storage_bucket.reports.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.run.member
}

# Model Monitoring runs as the Vertex AI service agent, which writes its output here.
resource "google_project_service_identity" "aiplatform" {
  provider = google-beta
  service  = "aiplatform.googleapis.com"
}

resource "google_storage_bucket_iam_member" "monitoring_writes_reports" {
  bucket = google_storage_bucket.reports.name
  role   = "roles/storage.objectAdmin"
  member = google_project_service_identity.aiplatform.member
}

# Cloud Scheduler starts the two monitoring jobs that the deploy job created.
resource "google_service_account" "scheduler" {
  account_id   = "example-model-scheduler"
  display_name = "Starts monitoring jobs"
}

resource "google_cloud_run_v2_job_iam_member" "scheduler_runs" {
  for_each = toset(["example-model-performance", "example-model-report"])
  location = var.region
  name     = each.value
  role     = "roles/run.invoker"
  member   = google_service_account.scheduler.member
}

resource "google_cloud_scheduler_job" "monitoring" {
  for_each = {
    "example-model-performance" = "0 7 * * 1" # Monday 07:00: last week's labeled predictions
    "example-model-report"      = "0 8 * * 1" # Monday 08:00: the Evidently report
  }
  name      = each.key
  region    = var.region
  schedule  = each.value
  time_zone = "America/New_York"
  http_target {
    http_method = "POST"
    uri         = "https://run.googleapis.com/v2/projects/${var.project}/locations/${var.region}/jobs/${each.key}:run"
    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }
}

# Performance alert: the latest weekly metric below its floor. Drift alerts come
# from Model Monitoring itself, by email. Triggered retraining, when wanted,
# subscribes to this policy's notification and submits the train pipeline; it
# never promotes.
resource "google_monitoring_notification_channel" "ml_alerts" {
  display_name = "ML alerts"
  type         = "email"
  labels       = { email_address = var.alert_email }
}

resource "google_monitoring_alert_policy" "performance" {
  display_name = "example-model performance below floor"
  combiner     = "OR"
  conditions {
    display_name = "roc_auc below floor"
    condition_threshold {
      filter          = "metric.type = \"custom.googleapis.com/example_model/roc_auc\" AND resource.type = \"global\""
      comparison      = "COMPARISON_LT"
      threshold_value = var.performance_floor
      duration        = "0s"
      aggregations {
        alignment_period   = "604800s"
        per_series_aligner = "ALIGN_MIN"
      }
    }
  }
  notification_channels = [google_monitoring_notification_channel.ml_alerts.id]
}

# ---- Project roles

resource "google_project_iam_member" "roles" {
  for_each = {
    "train-aiplatform"    = [google_service_account.train.member, "roles/aiplatform.user"]
    "train-bq-jobs"       = [google_service_account.train.member, "roles/bigquery.jobUser"]
    "train-bq-read"       = [google_service_account.train.member, "roles/bigquery.dataViewer"]
    "run-aiplatform"      = [google_service_account.run.member, "roles/aiplatform.viewer"]
    "run-bq-jobs"         = [google_service_account.run.member, "roles/bigquery.jobUser"]
    "run-bq-edit"         = [google_service_account.run.member, "roles/bigquery.dataEditor"]
    "run-metrics"         = [google_service_account.run.member, "roles/monitoring.metricWriter"]
    "deployer-run"        = [google_service_account.deployer.member, "roles/run.admin"]
    "deployer-aiplatform" = [google_service_account.deployer.member, "roles/aiplatform.user"]
  }
  project = var.project
  member  = each.value[0]
  role    = each.value[1]
}

# The deployer acts as the runtime identities when it deploys and submits.
resource "google_service_account_iam_member" "deployer_acts_as" {
  for_each = {
    run   = google_service_account.run.name
    train = google_service_account.train.name
  }
  service_account_id = each.value
  role               = "roles/iam.serviceAccountUser"
  member             = google_service_account.deployer.member
}

# ---- GitLab trust: release tags of one project, and nothing else, may deploy.

resource "google_iam_workload_identity_pool" "gitlab" {
  workload_identity_pool_id = "gitlab"
}

resource "google_iam_workload_identity_pool_provider" "gitlab" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.gitlab.workload_identity_pool_id
  workload_identity_pool_provider_id = "gitlab"
  attribute_mapping = {
    "google.subject"      = "assertion.sub"
    "attribute.project"   = "assertion.project_path"
    "attribute.ref_type"  = "assertion.ref_type"
    "attribute.ref"       = "assertion.ref"
    "attribute.protected" = "assertion.ref_protected"
  }
  attribute_condition = "assertion.project_path == '${var.gitlab_project_path}' && assertion.ref_type == 'tag' && assertion.ref_protected == 'true'"
  oidc {
    issuer_uri        = var.gitlab_url
    allowed_audiences = ["https://iam.googleapis.com/${google_iam_workload_identity_pool.gitlab.name}/providers/gitlab"]
  }
}

resource "google_service_account_iam_member" "gitlab_deployer" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gitlab.name}/attribute.project/${var.gitlab_project_path}"
}
