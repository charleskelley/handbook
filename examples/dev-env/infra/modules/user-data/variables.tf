variable "project" { type = string }

variable "location" {
  type    = string
  default = "US"
}

variable "users" {
  description = "Short name to email. The short name names the dataset and folder."
  type        = map(string)
}

variable "team_group" {
  description = "Google group with access to the shared team folder."
  type        = string
}

variable "bucket_name" { type = string }

variable "team_readers" {
  description = "Members outside the team that may read the team folder, such as the production training service account, which reads fixtures there."
  type        = list(string)
  default     = []
}

variable "table_expiration_days" {
  type    = number
  default = 180
}

variable "scratch_expiration_days" {
  type    = number
  default = 90
}

variable "kms_key" {
  description = "Customer-managed encryption key for the bucket, or null for Google-managed."
  type        = string
  default     = null
}
