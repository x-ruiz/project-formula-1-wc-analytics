resource "google_storage_bucket" "f1_wc_data_raw" {
  project       = var.project_name
  name          = "f1_wc_data_raw"
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

resource "google_storage_bucket" "f1_wc_data_curated" {
  project       = var.project_name
  name          = "f1_wc_data_curated"
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
