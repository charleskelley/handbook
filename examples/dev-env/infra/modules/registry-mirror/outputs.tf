output "image_prefix" {
  description = "Prefix for image references: append <artifactory-repo>/<image>:<tag>."
  value       = "${var.region}-docker.pkg.dev/${var.project}/${google_artifact_registry_repository.mirror.repository_id}"
}
