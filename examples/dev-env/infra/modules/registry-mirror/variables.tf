variable "project" { type = string }
variable "region" { type = string }

variable "repository_id" {
  type    = string
  default = "artifactory"
}

variable "artifactory_url" {
  description = "Artifactory base URL, such as https://artifactory.example.com."
  type        = string
}

variable "username" {
  description = "Artifactory user the token belongs to."
  type        = string
}

variable "password_secret" {
  description = "Secret Manager secret ID holding the Artifactory token, synced from the secret manager of record."
  type        = string
}

variable "password_secret_version" {
  description = "Full secret version name: projects/<p>/secrets/<id>/versions/latest."
  type        = string
}

variable "readers" {
  description = "Members that may pull, such as serviceAccount:run@<p>.iam.gserviceaccount.com."
  type        = list(string)
  default     = []
}
