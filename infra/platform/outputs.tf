output "bucket_f1_wc_1950_2020_name" {
  description = "Bucket for f1 kaggle data"
  value       = google_storage_bucket.f1_wc_1950_2020.name
}
