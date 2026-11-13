# One Cloud Workstation per person, all from one configuration. The container
# image is rebuilt by CI and recreated on every start; only /home persists, and
# /home holds code, environments, and caches, never data. Deleting a
# workstation deletes its home disk.

resource "google_workstations_workstation_cluster" "this" {
  provider               = google-beta
  project                = var.project
  location               = var.region
  workstation_cluster_id = var.cluster_id
  network                = var.network
  subnetwork             = var.subnetwork
}

resource "google_workstations_workstation_config" "dev" {
  provider               = google-beta
  project                = var.project
  location               = var.region
  workstation_cluster_id = google_workstations_workstation_cluster.this.workstation_cluster_id
  workstation_config_id  = "dev"
  idle_timeout           = "${var.idle_timeout_minutes * 60}s"
  running_timeout        = "${var.running_timeout_hours * 3600}s"

  host {
    gce_instance {
      machine_type                = var.machine_type
      boot_disk_size_gb           = 50
      service_account             = var.service_account
      disable_public_ip_addresses = true
    }
  }

  persistent_directories {
    mount_path = "/home"
    gce_pd {
      size_gb        = var.home_disk_gb
      fs_type        = "ext4"
      disk_type      = "pd-balanced"
      reclaim_policy = "DELETE"
    }
  }

  container {
    image = var.image
    env   = var.env
  }
}

resource "google_workstations_workstation" "user" {
  for_each               = var.users
  provider               = google-beta
  project                = var.project
  location               = var.region
  workstation_cluster_id = google_workstations_workstation_cluster.this.workstation_cluster_id
  workstation_config_id  = google_workstations_workstation_config.dev.workstation_config_id
  workstation_id         = each.key
  labels                 = { owner = each.key }
}

resource "google_workstations_workstation_iam_member" "user" {
  for_each               = var.users
  provider               = google-beta
  project                = var.project
  location               = var.region
  workstation_cluster_id = google_workstations_workstation_cluster.this.workstation_cluster_id
  workstation_config_id  = google_workstations_workstation_config.dev.workstation_config_id
  workstation_id         = google_workstations_workstation.user[each.key].workstation_id
  role                   = "roles/workstations.user"
  member                 = "user:${each.value}"
}
