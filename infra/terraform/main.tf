locals {
  prefix = "${var.project_name}-${var.environment}"
}

module "resource_group" {
  source   = "./modules/resource_group"
  name     = "rg-${local.prefix}"
  location = var.location
}

module "log_analytics" {
  source              = "./modules/log_analytics"
  name                = "law-${local.prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
}

module "key_vault" {
  source              = "./modules/key_vault"
  name                = "kv-${local.prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
}

module "container_apps" {
  source              = "./modules/container_apps"
  name                = "cae-${local.prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
  log_analytics_id    = module.log_analytics.workspace_id
}

module "networking" {
  source              = "./modules/networking"
  name                = local.prefix
  location            = var.location
  resource_group_name = module.resource_group.name
}

module "monitoring" {
  source              = "./modules/monitoring"
  name                = local.prefix
  location            = var.location
  resource_group_name = module.resource_group.name
  workspace_id        = module.log_analytics.workspace_id
}
