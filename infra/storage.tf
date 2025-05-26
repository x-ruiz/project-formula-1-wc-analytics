resource "google_storage_bucket" "f1_wc_1950_2020_raw" {
  project       = local.project
  name          = "f1_wc_1950_2020_raw"
  location      = "us-central1"
  force_destroy = true
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      matches_prefix = ["test"]
      age            = "1"
    }
  }
}
