output "bucket_f1_wc_data_raw_name" {
  description = "Bucket for f1 raw data"
  value       = google_storage_bucket.f1_wc_data_raw.name
}

output "bucket_f1_wc_data_curated_name" {
  description = "Bucket for f1 curated data"
  value       = google_storage_bucket.f1_wc_data_curated.name
}

