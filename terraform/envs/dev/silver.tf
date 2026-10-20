resource "fabric_lakehouse" "silver" {
  display_name = "lh_silver"
  workspace_id = fabric_workspace.this.id

  configuration = {
    enable_schemas = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Notebook definition comes from the Git-synced file, with workspace-specific IDs
# replaced by tokens, so the same file deploys to any workspace.
resource "fabric_notebook" "bronze_to_silver" {
  workspace_id              = fabric_workspace.this.id
  display_name              = "nb_bronze_to_silver"
  format                    = "py"
  definition_update_enabled = true

  definition = {
    "notebook-content.py" = {
      source = "${path.module}/files/nb_bronze_to_silver.py.tmpl"
      tokens = {
        WORKSPACE_ID   = fabric_workspace.this.id
        LAKEHOUSE_ID   = fabric_lakehouse.silver.id
        ENVIRONMENT_ID = fabric_environment.lending.id
      }
    }
  }

  depends_on = [fabric_spark_environment_settings.lending]
}
