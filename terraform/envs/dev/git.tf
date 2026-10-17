# GitHub connection: a Fabric "cloud connection" holding the PAT.
# key_wo is write-only: Terraform sends it but never stores it in state (Terraform >= 1.11).
resource "fabric_connection" "github" {
  display_name      = "conn-github-fabric-60"
  connectivity_type = "ShareableCloud"
  privacy_level     = "Organizational"

  connection_details = {
    type            = "GitHubSourceControl"
    creation_method = "GitHubSourceControl.Contents"
    parameters = [
      {
        name  = "url"
        value = var.github_repo_url
      }
    ]
  }

  credential_details = {
    credential_type = "Key"
    key_credentials = {
      key_wo         = var.github_pat
      key_wo_version = var.github_pat_version
    }
  }
}

# Connect the Terraform-managed workspace to its own folder in the repo.
resource "fabric_workspace_git" "this" {
  workspace_id            = fabric_workspace.this.id
  initialization_strategy = "PreferWorkspace"

  git_provider_details = {
    git_provider_type = "GitHub"
    owner_name        = var.github_owner
    repository_name   = var.github_repo
    branch_name       = var.github_branch
    directory_name    = "/fabric-items/iac-${var.environment}"
  }

  git_credentials = {
    source        = "ConfiguredConnection"
    connection_id = fabric_connection.github.id
  }
}
