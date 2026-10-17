# Source: the manually built bronze Lakehouse in the hands-on dev workspace.
# Looked up, not managed — Terraform must never modify or destroy it.
data "fabric_workspace" "source" {
  display_name = var.source_workspace_name
}

data "fabric_lakehouse" "source_bronze" {
  display_name = "lh_bronze"
  workspace_id = data.fabric_workspace.source.id
}

# Consumer Lakehouse in the Terraform-managed workspace.
resource "fabric_lakehouse" "consumer" {
  display_name = "lh_consumer"
  workspace_id = fabric_workspace.this.id

  configuration = {
    enable_schemas = true
  }

  # Lakehouses hold data; a force-new change must fail the plan, not delete it.
  lifecycle {
    prevent_destroy = true
  }
}

# Zero-copy pointer: lh_consumer/Tables/dbo/customers -> lh_bronze/Tables/raw/customers
resource "fabric_shortcut" "customers" {
  workspace_id = fabric_workspace.this.id
  item_id      = fabric_lakehouse.consumer.id
  path         = "Tables/dbo"
  name         = "customers"

  target = {
    onelake = {
      workspace_id = data.fabric_workspace.source.id
      item_id      = data.fabric_lakehouse.source_bronze.id
      path         = "Tables/raw/customers"
    }
  }
}
