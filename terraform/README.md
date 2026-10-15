# Terraform — Microsoft Fabric

Provisions the Fabric platform layer with the official `microsoft/fabric` provider.

| Managed by Terraform | Not managed here (and why) |
| --- | --- |
| Workspaces, capacity assignment | Tenant settings — no API support; set manually in Admin portal |
| Lakehouses (schema-enabled) | Lakehouse schemas/tables — created by Spark code |
| Workspace role assignments (groups) | Notebook/pipeline content — promoted via Git + fabric-cicd |

## Prerequisites
1. Tenant settings enabled: users can create Fabric items; service principals can use Fabric APIs.
2. Entra app registration exposing `api://fabric_terraform_provider/access`, pre-authorising Azure CLI.
3. Entra security group for engineers.
4. Login:
   ```
   az login --tenant <tenant-id> --allow-no-subscriptions --scope api://fabric_terraform_provider/.default
   ```

## Run
```
cd envs/dev
cp dev.tfvars.example dev.tfvars   # fill in values
terraform init
terraform plan  -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```
> Tested on a Fabric **trial** (FTL64) with Azure CLI user auth: workspace creation, capacity assignment and
> Lakehouse creation work, although the provider docs list trial capacity as unsupported. SPN auth on trial: TBD.

az login --tenant <tenant-id> --allow-no-subscriptions --scope api://<app-client-id>/.default