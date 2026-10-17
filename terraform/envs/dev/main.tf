# Capacity is looked up, not created: it is a trial (or pre-existing) capacity.
data "fabric_capacity" "this" {
  id = var.capacity_id

  lifecycle {
    postcondition {
      condition     = self.state == "Active"
      error_message = "Fabric capacity is not Active."
    }
  }
}

resource "fabric_workspace" "this" {
  display_name = "ws-fabrics-iac-${var.environment}"
  description  = "Terraform-managed workspace (${var.environment})"
  capacity_id  = data.fabric_capacity.this.id

  # NEW: Fabric-managed workspace identity (Entra service principal, no secrets)
  identity = {
    type = "SystemAssigned"
  }
}

# Portal enables schemas by default; the API does not. Changing this forces recreation.
resource "fabric_lakehouse" "bronze" {
  display_name = "lh_bronze"
  workspace_id = fabric_workspace.this.id

  configuration = {
    enable_schemas = true
  }
}

# Access through a group, never individual users.
resource "fabric_workspace_role_assignment" "engineers" {
  workspace_id = fabric_workspace.this.id
  role         = "Contributor"

  principal = {
    id   = var.engineers_group_id
    type = "Group"
  }
}