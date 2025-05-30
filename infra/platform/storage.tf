resource "google_storage_bucket" "f1_wc_data" {
  project       = var.project_name
  name          = "f1_wc_data"
  location      = var.primary_region
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
