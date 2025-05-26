
# --- Output the results from the external data source ---
output "gcs_prefix_discovery_result" {
  description = "The raw JSON output from the external script"
  value       = data.external.raw_f1_wc_1950_2020_prefixes.result
}
