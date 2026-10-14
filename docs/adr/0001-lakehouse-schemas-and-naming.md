# ADR-0001: Schema-enabled Lakehouses and naming convention

- **Status:** Accepted
- **Date:** 2026-10-14

## Context
Fabric Lakehouses can be created with or without schemas. Schema-enabled Lakehouses
group tables into namespaces (`raw`, `clean`, …), support four-part names
(`workspace.lakehouse.schema.table`), schema-level security and newer features such as
materialized lake views. The portal enables schemas by default, but the REST API
(used by Terraform) does **not** — it must be set explicitly.

## Options considered
1. **No schemas** — simpler, but a flat table list, no schema-level security, and no
   in-place migration path later.
2. **Schemas enabled** — small learning curve; required for several newer features.

## Decision
All Lakehouses are schema-enabled. Naming:

| Object | Convention | Example |
| --- | --- | --- |
| Workspace | `ws-<project>-<env>` | `ws-fabrics-handson-dev` |
| Lakehouse | `lh_<layer>` | `lh_bronze` |
| Warehouse | `wh_<layer>` | `wh_gold` |
| Schema | business area or stage | `raw`, `loans` |
| Notebook | `nb_<purpose>` | `nb_bronze_to_silver` |
| Pipeline | `pl_<purpose>` | `pl_ingest_loans` |

Item names use underscores because table and item names in some engines reject hyphens.

## Consequences
- Terraform must set `enable_schemas = true` on every `fabric_lakehouse`.
- Notebook code always references `schema.table`; a bare table name resolves to `dbo`.
