# fabric-60 — Microsoft Fabric platform, built by hand then as code

A BFSI loan-risk data platform on **Microsoft Fabric**, built over 60 days:
first configured manually in the portal to understand every setting, then
rebuilt from an empty tenant with **Terraform** and deployed through **GitHub Actions**.

> Status: Day 1 of 60 — see [build log](docs/build-log/)

## What this project demonstrates

| Area | What is covered |
| --- | --- |
| Platform administration | Entra roles, Fabric Administrator, tenant settings, capacity management |
| Data engineering | OneLake, Lakehouse (schemas), Spark notebooks, pipelines, medallion layers |
| Warehousing & BI | Warehouse (T-SQL), Direct Lake semantic models |
| Real-time | Eventstream, Eventhouse (KQL), Activator |
| Governance & security | Workspace roles, OneLake security, RLS/CLS, sensitivity labels |
| ML | MLflow experiments, model registry, batch scoring |
| CI/CD | Git integration, deployment pipelines, `fabric-cicd` |
| Infrastructure as code | `microsoft/fabric` Terraform provider, modules, OIDC |

## Architecture

_Diagram added as layers are built._

```
CSV / stream sources
   │
   ▼
lh_bronze (raw)  →  lh_silver (cleaned)  →  wh_gold (modelled)  →  Direct Lake report
                                        └→  ML model (default risk)
```

## Repository layout

```
docs/build-log/   day-by-day: what was built, why, what broke
docs/adr/         architecture decision records
docs/runbooks/    operational procedures
fabric-items/     item definitions synced by Fabric Git integration
terraform/        IaC for the platform
scripts/          utilities (synthetic data generator)
```

## Data

Synthetic Indian retail-lending data from `scripts/generate_loan_data.py`
(20,000 customers, ~50,000 loan applications) with deliberate data-quality issues
(duplicates, nulls, mixed date formats, inconsistent casing) to exercise cleaning logic.
No real customer data is used.

## Environment

- Personal Entra tenant, Fabric trial capacity
- Workspaces: `ws-fabrics-handson-dev`, `ws-fabrics-handson-prod`
