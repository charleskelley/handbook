variable "project" { type = string }
variable "zone" { type = string }
variable "subnetwork" { type = string }
variable "name" { type = string }

variable "owner_email" { type = string }

variable "owner_label" {
  description = "Owner as a label value: lowercase letters, digits, dashes."
  type        = string
}

variable "profile" {
  type    = string
  default = "cpu"
  validation {
    condition     = contains(["cpu", "gpu"], var.profile)
    error_message = "profile is cpu or gpu."
  }
}

variable "machine_type" {
  description = "For example n2-highmem-16 (128GB), n2-highmem-32 (256GB), or g2-standard-16 (one L4 GPU)."
  type        = string
}

variable "gpu_image" {
  description = "Deep Learning VM image or family with drivers matching the team's CUDA version. Required for gpu."
  type        = string
  default     = null
}

variable "boot_disk_gb" {
  type    = number
  default = 100
}

variable "service_account" { type = string }

variable "stop_schedule" {
  description = "Cron schedule for the daily stop. There is no option to turn it off."
  type        = string
  default     = "0 19 * * *"
}

variable "time_zone" {
  type    = string
  default = "America/New_York"
}

variable "artifactory_url" { type = string }
variable "artifactory_user" { type = string }

variable "artifactory_token_secret" {
  description = "Secret Manager secret ID holding a read-only Artifactory token."
  type        = string
}

variable "uv_version" { type = string }
