output "url" {
  description = "Set EXAMPLE_MODEL_TRACKING_URI to this."
  value       = google_cloud_run_v2_service.mlflow.uri
}

output "artifact_bucket" {
  value = google_storage_bucket.artifacts.name
}
