# Day 0 — Setup (13 Oct 2026)

## Environment
- Tenant: vivekkumard9797gmail.onmicrosoft.com (607395d0-ca31-42b1-b67b-0a36385fca6f)
- Working user: vivekvc97@vivekkumard9797gmail.onmicrosoft.com
- Admin role: Fabric Administrator on vivekvc97 (assigned by the Gmail Global Admin account)
- Trial: __ CU, region __, 59 days left on 13 Oct 2026
- Workspaces: ws-fabrics-handson-dev, ws-fabrics-handson-prod (Fabric Trial)
- Tenant settings enabled: create Fabric items, SPN access to Fabric APIs, Git sync, GitHub sync
- Tools: Fabric CLI 1.7.0 (+ fabric-cicd 1.3.0), Azure CLI, Terraform, Python 3.12
- Capacity Metrics app installed (creates its own workspace — leave it alone)

## Lessons
- A personal Azure tenant makes the Gmail login a Global Admin (#EXT# guest-style UPN).
  Fabric needs a member user (onmicrosoft.com); new users get NO roles by default.
- Assigned Fabric Administrator, not Global Admin → least privilege.
- `fab auth login` on Windows uses the account broker dialog (pymsalruntime);
  it hides behind VS Code → run from standalone PowerShell.
- `az login --allow-no-subscriptions` works for Fabric: Fabric APIs are tenant-scoped, not subscription-scoped.
  At the subscription prompt press Enter (typing 1 gives "Invalid selection").

## To codify in Terraform later
- Workspaces + capacity assignment (fabric_workspace, data "fabric_capacity")
- Tenant settings are NOT Terraform-managed → document them as a manual prerequisite
