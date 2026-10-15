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
