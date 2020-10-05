data "archive_file" "zip_main" {
  type        = "zip"
  source_dir  = "./functions/${var.function}/"
  output_path = "./functions/${var.function}.zip"
}


resource "google_storage_bucket_object" "function_archive" {
  name         = "${var.function}.zip"
  bucket       = var.project.function_bucket
  source       = "./functions/${var.function}.zip"
  content_type = "application/zip"
  depends_on = [
    data.archive_file.zip_main
  ]
}


resource "google_cloudfunctions_function" "function" {
  name    = var.function
  project = var.project.name
  region  = var.region

  runtime             = "python37"
  available_memory_mb = 256

  entry_point  = "main"
  trigger_http = true

  source_archive_bucket = var.project.function_bucket
  source_archive_object = "${var.function}.zip"

  depends_on = [
  google_storage_bucket_object.function_archive]
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project.name
  region         = var.region
  cloud_function = var.function

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"

  depends_on = [google_cloudfunctions_function.function]
}
