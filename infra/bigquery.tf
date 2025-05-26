resource "google_bigquery_dataset" "f1_wc_1950_2020_raw" {
    project = local.project
    dataset_id = "f1_wc_1950_2020_raw"
    friendly_name = "f1_wc_1950_2020_raw"
    location = "us-central1"
}

resource "google_bigquery_table" "circuits_raw" {
    dataset_id = google_bigquery_dataset.f1_wc_1950_2020_raw.dataset_id
    table_id = "circuits_raw"

    external_data_configuration {
      autodetect = true
      source_format = "PARQUET"

      source_uris = [ "gs://f1_wc_1950_2020_raw/test/circuits.parquet" ]
    }
}