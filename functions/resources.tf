module "functions" {
  source     = "./functions"
  project    = var.project
  region     = var.region
  function   = each.value
  for_each   = toset(var.functions)
  depends_on = [google_storage_bucket.function_source_bucket]
}
