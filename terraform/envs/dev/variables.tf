variable "tenant_id" {
  description = "Entra ID tenant ID"
  type        = string
}

variable "capacity_id" {
  description = "Fabric capacity ID the workspace is assigned to"
  type        = string
}

variable "environment" {
  description = "Environment suffix used in names (dev, prod)"
  type        = string
}

variable "engineers_group_id" {
  description = "Object ID of the Entra security group granted Contributor on the workspace"
  type        = string
}
