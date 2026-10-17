variable "github_owner" {
  description = "GitHub user or organisation that owns the repo"
  type        = string
}

variable "github_repo" {
  description = "Repository name"
  type        = string
}

variable "github_repo_url" {
  description = "Full repository URL, scopes the connection to one repo"
  type        = string
}

variable "github_branch" {
  description = "Branch the workspace syncs with"
  type        = string
  default     = "main"
}

variable "github_pat" {
  description = "Fine-grained GitHub PAT (Contents: read/write). Supply via TF_VAR_github_pat, never in tfvars."
  type        = string
  sensitive   = true
  ephemeral   = true
}

variable "github_pat_version" {
  description = "Increment when rotating the PAT so Terraform re-sends it"
  type        = number
  default     = 1
}
