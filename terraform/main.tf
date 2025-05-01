resource "google_dataproc_cluster" "simplecluster" {
  name   = "simplecluster"
  region = "us-central1"

  depends_on = [ google_project_service.dataproc-api ]
}

resource "google_project_service" "dataproc-api" {
  project = local.project_id
  service = "dataproc.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_on_destroy = true
}