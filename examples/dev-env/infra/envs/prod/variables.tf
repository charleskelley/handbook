variable "project" {
  description = "The prod project. Only CI and service accounts act here."
  type        = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "artifactory_url" { type = string }

variable "artifactory_release_user" {
  description = "Artifactory user that can read the release repositories and nothing else."
  type        = string
}

variable "artifactory_token_secret" {
  description = "Secret Manager secret ID with that user's token, synced from CyberArk."
  type        = string
}

variable "gitlab_url" {
  type    = string
  default = "https://gitlab.example.com"
}

variable "gitlab_project_path" {
  description = "Only release tags from this project may deploy, for example ds/example-model."
  type        = string
}

variable "models_bucket" { type = string }
variable "pipelines_bucket" { type = string }
variable "reports_bucket" { type = string }

variable "alert_email" {
  description = "Where performance and drift alerts go, such as a team list."
  type        = string
}

variable "performance_floor" {
  description = "Alert when the weekly roc_auc of any version falls below this. Matches monitoring.alert_floor in the model config."
  type        = number
  default     = 0.7
}
