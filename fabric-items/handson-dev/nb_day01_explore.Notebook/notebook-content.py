# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "cae26a9e-0f3c-4c49-97bb-629982ebd7bf",
# META       "default_lakehouse_name": "lh_bronze",
# META       "default_lakehouse_workspace_id": "56a2cb46-2be9-470c-bf92-ed674b0753f6",
# META       "known_lakehouses": [
# META         {
# META           "id": "cae26a9e-0f3c-4c49-97bb-629982ebd7bf"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Cell 1: where does the table actually live?
detail = spark.sql("DESCRIBE DETAIL raw.loan_applications").collect()[0]
print("format   :", detail["format"])
print("location :", detail["location"])
print("numFiles :", detail["numFiles"])
print("sizeInMB :", round(detail["sizeInBytes"] / 1024 / 1024, 2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 2: list the files behind the table
for f in notebookutils.fs.ls(detail["location"]):
    print(f"{f.name:<60} {f.size:>12,}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 3: look inside the transaction log
for f in notebookutils.fs.ls(detail["location"] + "/_delta_log"):
    print(f.name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Cell 4: scratch copy (CTAS = Create Table As Select)
# MAGIC CREATE OR REPLACE TABLE raw.scratch_loans AS
# MAGIC SELECT * FROM raw.loan_applications

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Cell 5: the DELETE that failed in the SQL endpoint, now via Spark
# MAGIC DELETE FROM raw.scratch_loans WHERE CAST(loan_amount AS DOUBLE) < 0

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Cell 6: history: one row per commit
# MAGIC DESCRIBE HISTORY raw.scratch_loans

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Cell 7: time travel: compare current table with version 0
# MAGIC SELECT 'now' AS version, COUNT(*) AS rows FROM raw.scratch_loans
# MAGIC UNION ALL
# MAGIC SELECT 'v0', COUNT(*) FROM raw.scratch_loans VERSION AS OF 0

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Cell 8: clean up
# MAGIC DROP TABLE raw.scratch_loans

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 9: Spark write defaults for this workspace
for key in ["spark.fabric.resourceProfile",
            "spark.sql.parquet.vorder.default",
            "spark.databricks.delta.optimizeWrite.enabled"]:
    print(f"{key:<48} {spark.conf.get(key, 'not set')}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
