# Where development datasets live: a BigQuery dataset per person and a managed
# folder per person in one governed bucket. Both expire on their own, so working
# data does not pile up. Anything worth keeping moves to a team dataset or the
# team folder.

resource "google_bigquery_dataset" "user" {
  for_each                    = var.users
  project                     = var.project
  dataset_id                  = "dev_${replace(each.key, "-", "_")}"
  location                    = var.location
  default_table_expiration_ms = var.table_expiration_days * 24 * 60 * 60 * 1000
  labels                      = { owner = each.key }
}

resource "google_bigquery_dataset_iam_member" "user" {
  for_each   = var.users
  project    = var.project
  dataset_id = google_bigquery_dataset.user[each.key].dataset_id
  role       = "roles/bigquery.dataOwner"
  member     = "user:${each.value}"
}

resource "google_project_iam_member" "bigquery_jobs" {
  for_each = var.users
  project  = var.project
  role     = "roles/bigquery.jobUser"
  member   = "user:${each.value}"
}

resource "google_storage_bucket" "dev" {
  project                     = var.project
  name                        = var.bucket_name
  location                    = var.location
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  dynamic "encryption" {
    for_each = var.kms_key == null ? [] : [var.kms_key]
    content {
      default_kms_key_name = encryption.value
    }
  }

  lifecycle_rule {
    condition {
      age            = var.scratch_expiration_days
      matches_prefix = ["users/"]
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_managed_folder" "user" {
  for_each = var.users
  bucket   = google_storage_bucket.dev.name
  name     = "users/${each.key}/"
}

resource "google_storage_managed_folder_iam_member" "user" {
  for_each       = var.users
  bucket         = google_storage_bucket.dev.name
  managed_folder = google_storage_managed_folder.user[each.key].name
  role           = "roles/storage.objectUser"
  member         = "user:${each.value}"
}

resource "google_storage_managed_folder" "team" {
  bucket = google_storage_bucket.dev.name
  name   = "team/"
}

resource "google_storage_managed_folder_iam_member" "team" {
  bucket         = google_storage_bucket.dev.name
  managed_folder = google_storage_managed_folder.team.name
  role           = "roles/storage.objectUser"
  member         = "group:${var.team_group}"
}

resource "google_storage_managed_folder_iam_member" "team_readers" {
  for_each       = toset(var.team_readers)
  bucket         = google_storage_bucket.dev.name
  managed_folder = google_storage_managed_folder.team.name
  role           = "roles/storage.objectViewer"
  member         = each.value
}
