provider "google" {
  project = "formula-1-wc-analytics"
  region  = "us-central1"
  zone    = "us-central1-c"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.27.0"
    }
  }

  backend "gcs" {
    bucket = "tf-state-dv-f1"
    prefix = "terraform/state"
  }
}