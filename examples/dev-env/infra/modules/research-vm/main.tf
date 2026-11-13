# A large-memory or GPU research VM for one person, in the dev project. It is
# disposable: the startup script rebuilds its wiring at every boot, code lives in
# git, and data lives in BigQuery and the governed bucket. It always stops on a
# schedule. Production never runs on these, or on images made from them.

locals {
  region = join("-", slice(split("-", var.zone), 0, 2))
  gpu    = var.profile == "gpu"
  image  = local.gpu ? var.gpu_image : "debian-cloud/debian-12"
}

resource "google_compute_resource_policy" "stop" {
  project = var.project
  name    = "${var.name}-stop"
  region  = local.region

  instance_schedule_policy {
    time_zone = var.time_zone
    vm_stop_schedule {
      schedule = var.stop_schedule
    }
  }
}

resource "google_compute_instance" "this" {
  project      = var.project
  name         = var.name
  zone         = var.zone
  machine_type = var.machine_type
  tags         = ["research-vm"]
  labels       = { owner = var.owner_label, profile = var.profile }

  boot_disk {
    initialize_params {
      image = local.image
      size  = var.boot_disk_gb
      type  = "pd-balanced"
    }
  }

  # No external IP: SSH arrives through IAP, packages through Cloud NAT to Artifactory.
  network_interface {
    subnetwork = var.subnetwork
  }

  service_account {
    email  = var.service_account
    scopes = ["cloud-platform"]
  }

  scheduling {
    # GPUs cannot live-migrate.
    on_host_maintenance = local.gpu ? "TERMINATE" : "MIGRATE"
  }

  shielded_instance_config {
    enable_secure_boot = !local.gpu
  }

  metadata = {
    enable-oslogin = "TRUE"
    startup-script = templatefile("${path.module}/startup.sh.tftpl", {
      artifactory_url  = var.artifactory_url
      artifactory_user = var.artifactory_user
      token_secret     = var.artifactory_token_secret
      uv_version       = var.uv_version
    })
  }

  resource_policies = [google_compute_resource_policy.stop.id]

  lifecycle {
    precondition {
      condition     = !local.gpu || (var.gpu_image != null && can(regex("^(g2|a2|a3)-", var.machine_type)))
      error_message = "The gpu profile needs gpu_image and an accelerator-optimized machine type (g2, a2, a3)."
    }
  }
}

resource "google_compute_instance_iam_member" "os_login" {
  project       = var.project
  zone          = var.zone
  instance_name = google_compute_instance.this.name
  role          = "roles/compute.osLogin"
  member        = "user:${var.owner_email}"
}

resource "google_iap_tunnel_instance_iam_member" "tunnel" {
  project  = var.project
  zone     = var.zone
  instance = google_compute_instance.this.name
  role     = "roles/iap.tunnelResourceAccessor"
  member   = "user:${var.owner_email}"
}
