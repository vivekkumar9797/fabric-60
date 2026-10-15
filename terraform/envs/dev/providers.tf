# Auth: Azure CLI user context.
# Requires an Entra app registration exposing api://fabric_terraform_provider/access
# and: az login --tenant <tenant> --allow-no-subscriptions --scope api://fabric_terraform_provider/.default
provider "fabric" {
  use_cli   = true
  tenant_id = var.tenant_id
}
