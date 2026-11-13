# Artifactory repositories. Applied by whoever administers Artifactory, from CI,
# with the admin token supplied as ARTIFACTORY_ACCESS_TOKEN.

terraform {
  required_version = ">= 1.6"
  required_providers {
    artifactory = { source = "jfrog/artifactory", version = ">= 12.0" }
  }
}

variable "artifactory_url" {
  type    = string
  default = "https://artifactory.example.com"
}

provider "artifactory" {
  url = var.artifactory_url
}

module "repositories" {
  source = "../../modules/artifactory"
}
