variable "spark_runtime_version" {
  description = "Fabric Spark runtime (1.1, 1.2, 1.3, 2.0). Match what env_lending_dev uses in the portal."
  type        = string
  default     = "1.3"
}
