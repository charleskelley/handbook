variable "project" {
  description = "The dev project. People can create and use resources here; never in prod."
  type        = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "network" { type = string }
variable "subnetwork" { type = string }

variable "users" {
  description = "Everyone on the team. A research_vm entry gives that person a research VM."
  type = map(object({
    email = string
    research_vm = optional(object({
      profile      = optional(string, "cpu")
      machine_type = string
    }))
  }))
}

variable "team_group" { type = string }
variable "dev_bucket" { type = string }

variable "artifactory_url" { type = string }

variable "artifactory_user" {
  description = "Read-only Artifactory user for dev machines and the registry mirror."
  type        = string
}

variable "artifactory_token_secret" {
  description = "Secret Manager secret ID with that user's token, synced from CyberArk."
  type        = string
}

variable "workstation_image_tag" { type = string }

variable "gpu_image" {
  description = "Deep Learning VM image or family for GPU research VMs."
  type        = string
  default     = null
}

variable "uv_version" { type = string }

variable "mlflow_image_tag" {
  description = "Tag of the MLflow server image built by mlflow-image/.gitlab-ci.yml."
  type        = string
}

variable "prod_train_service_account" {
  description = "The production training service account, which logs its runs here."
  type        = string
}
