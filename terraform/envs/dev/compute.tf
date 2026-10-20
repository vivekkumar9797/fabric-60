# Prerequisite (manual, capacity admin): "Customized workspace pools" enabled on the capacity.

resource "fabric_spark_custom_pool" "small" {
  workspace_id = fabric_workspace.this.id
  name         = "pool-small-${var.environment}"
  type         = "Workspace"
  node_family  = "MemoryOptimized"
  node_size    = "Small"

  auto_scale = {
    enabled        = true
    min_node_count = 1
    max_node_count = 3
  }

  dynamic_executor_allocation = {
    enabled       = true
    min_executors = 1
    max_executors = 2
  }
}

resource "fabric_environment" "lending" {
  workspace_id = fabric_workspace.this.id
  display_name = "env_lending_${var.environment}"
  description  = "Spark compute + properties for the lending pipelines"
}

resource "fabric_spark_environment_settings" "lending" {
  workspace_id       = fabric_workspace.this.id
  environment_id     = fabric_environment.lending.id
  publication_status = "Published"
  runtime_version    = var.spark_runtime_version

  driver_cores    = 4
  driver_memory   = "28g"
  executor_cores  = 4
  executor_memory = "28g"

  dynamic_executor_allocation = {
    enabled       = true
    min_executors = 1
    max_executors = 2
  }

  pool = {
    name = fabric_spark_custom_pool.small.name
    type = "Workspace"
  }

  spark_properties = {
    "spark.fabric.resourceProfile" = "writeHeavy"
  }
}

resource "fabric_spark_workspace_settings" "this" {
  workspace_id = fabric_workspace.this.id

  environment = {
    name            = fabric_environment.lending.display_name
    runtime_version = var.spark_runtime_version
  }

  pool = {
    customize_compute_enabled = true
    default_pool = {
      name = "Starter Pool"
      type = "Workspace"
    }
  }

  high_concurrency = {
    notebook_interactive_run_enabled = true
    notebook_pipeline_run_enabled    = true
  }

  job = {
    session_timeout_in_minutes = 20
  }

  depends_on = [fabric_spark_environment_settings.lending]
}
