output "mlflow_url" {
  description = "The tracking server. Goes in every .env and in the CI variable MLFLOW_URL."
  value       = module.mlflow.url
}
