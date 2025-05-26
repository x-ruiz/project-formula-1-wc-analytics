resource "google_storage_bucket" "f1_wc_1950_2020" {
  project       = var.project_name
  name          = "f1_wc_1950_2020"
  location      = "us-central1"
  force_destroy = true
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      matches_prefix = ["staging"]
      age            = "1"
    }
  }
}
