provider "google" {
  credentials = file("<CREDENTIALS_FILE>.json")
  project = var.project.name
  region = var.region
}

resource "google_storage_bucket" "function_source_bucket" {
  name = var.project.function_bucket
  force_destroy = true
  location = var.region
  uniform_bucket_level_access = true
  project = var.project.name
}
