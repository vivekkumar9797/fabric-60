# Day 1 — Lakehouse and OneLake (14 Oct 2026)

## Built
- `lh_bronze` (schemas enabled) in `ws-fabrics-handson-dev`
- Schema `raw`; folder `Files/landing/loans`
- Tables: `raw.customers` (__ rows), `raw.loan_applications` (__ rows)
- Notebook `nb_day01_explore`

## Observations
- Trial capacity: __ CU, region __
- Items created with the Lakehouse: __
- Types inferred by Load to tables:
  - `application_date`: __
  - `defaulted`: __
  - `annual_income`: __
- `DELETE` on SQL analytics endpoint: __ (error text: __)
- V-Order setting in this workspace: __ ; resource profile: __
- Delta history after Load to tables: __ version(s), operation __

## Why it matters
- Load to tables has no schema control → production loads are notebook/pipeline code
- SQL analytics endpoint is read-only → writes go through Spark or a Warehouse
- Data is open Delta/Parquet in OneLake → readable by any Delta engine via abfss://

## To codify in Terraform
- `fabric_lakehouse` with `enable_schemas = true` (API default is false)
- Workspace Spark settings: resource profile / V-Order decision
- File uploads and table loads are NOT infrastructure → pipeline/notebook code

## Self-test
1. What does creating a Lakehouse produce?
2. Files vs Tables — what lives where, and what is SQL-queryable?
3. Why can't you DELETE through the SQL analytics endpoint?
4. Why does a Terraform-created Lakehouse differ from a portal one?
5. How would a Databricks team read this table without copying it?
