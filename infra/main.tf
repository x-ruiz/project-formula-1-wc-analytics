locals {
  # Parse the raw data prefixes from f1_wc_1950_2020 bucket to a map for iteration
  f1_wc_1950_2020_raw_prefix_output = data.external.raw_f1_wc_1950_2020_prefixes.result.all_prefixes_json
  f1_wc_1950_2020_raw_prefix_set    = (local.f1_wc_1950_2020_raw_prefix_output == "") ? [] : toset(jsondecode(local.f1_wc_1950_2020_raw_prefix_output))
}

module "platform" {
  source       = "./platform"
  project_name = local.project
}

module "bigquery_dynamic" {
  source       = "./bigquery_dynamic"
  project_name = local.project
  raw_prefixes = local.f1_wc_1950_2020_raw_prefix_set
  depends_on   = [module.platform]
}


# Get all the prefixes for raw data in the f1_wc_1950_2020 bucket
data "external" "raw_f1_wc_1950_2020_prefixes" {
  program = ["python3", "${path.module}/scripts/list_gcs_prefix.py"]
  query = {
    "bucket_name" = module.platform.bucket_f1_wc_1950_2020_name
    "prefix"      = "raw"
  }
}

