variable "project" { type = string }
variable "region" { type = string }
variable "network" { type = string }
variable "subnetwork" { type = string }

variable "cluster_id" {
  type    = string
  default = "dev"
}

variable "users" {
  description = "Workstation ID to the owner's email."
  type        = map(string)
}

variable "image" {
  description = "Workstation image, pulled through the Artifact Registry mirror of Artifactory."
  type        = string
}

variable "env" {
  description = "Environment for the workstation container, such as Artifactory settings."
  type        = map(string)
  default     = {}
}

variable "service_account" {
  description = "Workstation VM identity. It reads the Artifactory token; people use their own credentials for data."
  type        = string
}

variable "machine_type" {
  description = "Small: daily development. Large-memory work goes to research VMs or Vertex AI jobs."
  type        = string
  default     = "e2-standard-8"
}

variable "home_disk_gb" {
  type    = number
  default = 100
}

variable "idle_timeout_minutes" {
  type    = number
  default = 60
}

variable "running_timeout_hours" {
  type    = number
  default = 12
}
