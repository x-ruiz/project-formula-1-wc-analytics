resource "google_bigquery_dataset" "f1_wc_1950_2020_raw" {
  project       = var.project_name
  dataset_id    = "f1_wc_1950_2020_raw"
  friendly_name = "f1_wc_1950_2020_raw"
  location      = "us-central1"
}

resource "google_bigquery_table" "f1_wc_1950_2020_raw" {
  # set of prefixes under raw prefix
  # example: circuits, races, etc.
  for_each = var.raw_prefixes

  dataset_id          = google_bigquery_dataset.f1_wc_1950_2020_raw.dataset_id
  table_id            = "${each.value}_raw"
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"

    source_uris = ["gs://f1_wc_1950_2020/raw/${each.value}/dt=*/data.parquet"]

    hive_partitioning_options {
      mode                     = "STRINGS"
      source_uri_prefix        = "gs://f1_wc_1950_2020/raw/${each.value}"
      require_partition_filter = true
    }
  }
}
