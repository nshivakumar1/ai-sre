variable "location" {
  type        = string
  description = "Azure region to deploy resources into"
  default     = "centralindia"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g. dev, prod)"
  default     = "dev"
}

variable "project_name" {
  type        = string
  description = "Name of the project"
  default     = "aisre"
}
