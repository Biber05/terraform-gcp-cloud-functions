variable "project" {
  type = object({
    name : string,
    url : string,
    function_bucket : string
  })
}

variable "region" {
  type = string
}

variable "function" {
  type = string
}
