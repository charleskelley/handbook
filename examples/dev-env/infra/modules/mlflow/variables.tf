variable "project" { type = string }
variable "region" { type = string }

variable "network" {
  description = "VPC self link for the Cloud SQL private IP."
  type        = string
}

variable "image" {
  description = "The MLflow server image, pulled through the Artifact Registry mirror of Artifactory."
  type        = string
}

variable "artifact_bucket" {
  description = "Bucket name for run artifacts: plots, summaries, small models."
  type        = string
}

variable "database_tier" {
  description = "Cloud SQL machine tier. The smallest shared-core tier is enough for a team."
  type        = string
  default     = "db-f1-micro"
}

variable "invokers" {
  description = "Members allowed to call the server: the team group and the production training service account."
  type        = list(string)
}
