variable "name" {
  description = "The name of the Application Insights resource."
  type        = string
}

variable "location" {
  description = "The Azure region."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "workspace_id" {
  description = "The ID of the Log Analytics Workspace to link to."
  type        = string
}
