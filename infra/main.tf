locals {
  # API management
  api_list = toset([
    "dataplex.googleapis.com",
    "bigquery.googleapis.com"
  ])
}

module "platform" {
  source       = "./platform"
  project_name = local.project
}

# Enable Project APIs
resource "google_project_service" "project_apis" {
  for_each = local.api_list

  project = local.project
  service = each.value
}
