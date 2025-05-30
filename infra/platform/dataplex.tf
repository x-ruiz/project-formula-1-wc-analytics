resource "google_dataplex_lake" "primary" {
  location     = var.primary_region
  name         = "f1-wc-lake"
  display_name = "F1 WC Data Lake"
  description  = "Data lake to hold data related to formula 1"
  project      = var.project_name
}

resource "google_dataplex_zone" "raw_zone" {
  discovery_spec {
    enabled = true
  }

  lake     = google_dataplex_lake.primary.name
  location = var.primary_region
  name     = "raw-zone"

  resource_spec {
    location_type = "SINGLE_REGION"
  }

  type         = "RAW"
  description  = "Raw Zone for F1 WC Data"
  display_name = "F1 WC Data Raw"
  project      = var.project_name
  labels       = {}
}

resource "google_dataplex_asset" "raw_bucket" {
  name     = replace(google_storage_bucket.f1_wc_data.name, "_", "-")
  location = var.primary_region

  lake          = google_dataplex_lake.primary.name
  dataplex_zone = google_dataplex_zone.raw_zone.name

  discovery_spec {
    enabled = true
  }

  resource_spec {
    name = "projects/${var.project_name}/buckets/${google_storage_bucket.f1_wc_data.name}"
    type = "STORAGE_BUCKET"
  }

  #   labels = {
  #     env      = "foo"
  #     my-asset = "exists"
  #   }


  project = var.project_name
  depends_on = [
    google_storage_bucket.f1_wc_data
  ]
}
