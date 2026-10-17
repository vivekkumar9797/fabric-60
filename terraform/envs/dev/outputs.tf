output "capacity_sku" {
  value = data.fabric_capacity.this.sku
}

output "capacity_region" {
  value = data.fabric_capacity.this.region
}

output "workspace_id" {
  value = fabric_workspace.this.id
}

output "lakehouse_id" {
  value = fabric_lakehouse.bronze.id
}

# NEW: the workspace identity's service principal ID in Entra
output "workspace_identity_sp_id" {
  value = fabric_workspace.this.identity.service_principal_id
}