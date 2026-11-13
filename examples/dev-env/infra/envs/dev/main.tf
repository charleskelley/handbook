# The dev project: a workstation for everyone, research VMs for some, and the
# governed places where development data lives.

locals {
  emails = { for name, user in var.users : name => user.email }
}

resource "google_service_account" "workstation" {
  account_id   = "dev-workstation"
  display_name = "Cloud Workstations host"
}

resource "google_service_account" "research_vm" {
  account_id   = "dev-research-vm"
  display_name = "Research VMs"
}

# Both identities read the read-only Artifactory token and nothing else. People
# reach data with their own credentials (`gcloud auth login` on the machine).
resource "google_secret_manager_secret_iam_member" "artifactory_token" {
  for_each = {
    workstation = google_service_account.workstation.member
    research_vm = google_service_account.research_vm.member
  }
  secret_id = var.artifactory_token_secret
  role      = "roles/secretmanager.secretAccessor"
  member    = each.value
}

module "registry_mirror" {
  source                  = "../../modules/registry-mirror"
  project                 = var.project
  region                  = var.region
  artifactory_url         = var.artifactory_url
  username                = var.artifactory_user
  password_secret         = var.artifactory_token_secret
  password_secret_version = "projects/${var.project}/secrets/${var.artifactory_token_secret}/versions/latest"
  readers                 = [google_service_account.workstation.member]
}

module "workstations" {
  source          = "../../modules/workstations"
  project         = var.project
  region          = var.region
  network         = var.network
  subnetwork      = var.subnetwork
  users           = local.emails
  service_account = google_service_account.workstation.email
  image           = "${module.registry_mirror.image_prefix}/docker-dev/workstation:${var.workstation_image_tag}"
  env = {
    ARTIFACTORY_URL          = var.artifactory_url
    ARTIFACTORY_USER         = var.artifactory_user
    ARTIFACTORY_TOKEN_SECRET = var.artifactory_token_secret
  }
}

# Experiment tracking. Research and the production pipeline log to the same
# server, so a research run and the run that reproduced it sit side by side.
module "mlflow" {
  source          = "../../modules/mlflow"
  project         = var.project
  region          = var.region
  network         = var.network
  image           = "${module.registry_mirror.image_prefix}/docker-dev/mlflow:${var.mlflow_image_tag}"
  artifact_bucket = "${var.project}-mlflow-artifacts"
  invokers = [
    "group:${var.team_group}",
    "serviceAccount:${var.prod_train_service_account}",
  ]
}

module "user_data" {
  source      = "../../modules/user-data"
  project     = var.project
  users       = local.emails
  team_group  = var.team_group
  bucket_name = var.dev_bucket
  # Production training scores research fixtures saved under team/fixtures/.
  team_readers = ["serviceAccount:${var.prod_train_service_account}"]
}

module "research_vm" {
  source   = "../../modules/research-vm"
  for_each = { for name, user in var.users : name => user if user.research_vm != null }

  project                  = var.project
  zone                     = var.zone
  subnetwork               = var.subnetwork
  name                     = "research-${each.key}"
  owner_email              = each.value.email
  owner_label              = each.key
  profile                  = each.value.research_vm.profile
  machine_type             = each.value.research_vm.machine_type
  gpu_image                = var.gpu_image
  service_account          = google_service_account.research_vm.email
  artifactory_url          = var.artifactory_url
  artifactory_user         = var.artifactory_user
  artifactory_token_secret = var.artifactory_token_secret
  uv_version               = var.uv_version
}

# OS Login on a VM with a service account needs permission to act as it.
resource "google_service_account_iam_member" "research_vm_users" {
  for_each           = module.research_vm
  service_account_id = google_service_account.research_vm.name
  role               = "roles/iam.serviceAccountUser"
  member             = "user:${var.users[each.key].email}"
}

# SSH reaches research VMs only through IAP's address range.
resource "google_compute_firewall" "iap_ssh" {
  name          = "allow-iap-ssh-research"
  network       = var.network
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["research-vm"]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
