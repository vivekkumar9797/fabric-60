# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "28616a96-458f-429f-8fdd-ac25663ce5c5",
# META       "default_lakehouse_name": "lh_silver",
# META       "default_lakehouse_workspace_id": "56a2cb46-2be9-470c-bf92-ed674b0753f6",
# META       "known_lakehouses": [
# META         {
# META           "id": "28616a96-458f-429f-8fdd-ac25663ce5c5"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "6e5ec385-a222-9d98-4a8f-7da38aff99fc",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

# ---------- CELL 1 (PARAMETERS) ----------
# In Fabric: cell "..." menu -> "Toggle parameter cell".
# Pipelines override these values at run time.
run_date = "2026-10-20"
source_lakehouse = "lh_bronze"
source_schema = "raw"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# ---------- CELL 2 : runtime facts (prove the environment is applied) ----------
for k in ["spark.fabric.resourceProfile", "spark.sql.parquet.vorder.default"]:
    print(k, "=", spark.conf.get(k, "not set"))
print("Spark version:", spark.version)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ---------- CELL 3 : schemas ----------
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS quarantine")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# ---------- CELL 4 : customers -> silver.customers ----------
from pyspark.sql import functions as F

src = f"{source_lakehouse}.{source_schema}"

customers = (
    spark.table(f"{src}.customers")
    .withColumn("city", F.initcap(F.trim(F.col("city"))))
    .withColumn("date_of_birth", F.to_date("date_of_birth"))
    .withColumn("customer_since", F.to_date("customer_since"))
    .withColumn("annual_income", F.col("annual_income").cast("decimal(14,2)"))
    .withColumn("cibil_score", F.col("cibil_score").cast("int"))
    .withColumn("_run_date", F.lit(run_date).cast("date"))
    .dropDuplicates(["customer_id"])
)

(customers.write.mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("silver.customers"))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ---------- CELL 5 : loan applications -> silver + quarantine ----------
apps = (
    spark.table(f"{src}.loan_applications")
    .withColumn("application_date",
        F.coalesce(F.to_date(F.col("application_date").cast("string"), "yyyy-MM-dd"),
                   F.to_date(F.col("application_date").cast("string"), "dd/MM/yyyy")))
    .withColumn("loan_amount", F.col("loan_amount").cast("decimal(14,2)"))
    .withColumn("interest_rate", F.col("interest_rate").cast("decimal(5,2)"))
    .withColumn("tenure_months", F.col("tenure_months").cast("int"))
    .withColumn("existing_emi_monthly", F.col("existing_emi_monthly").cast("decimal(12,2)"))
    .withColumn("defaulted", F.col("defaulted").cast("int"))
    .withColumn("_run_date", F.lit(run_date).cast("date"))
    .dropDuplicates(["application_id"])
)

is_valid = (F.col("loan_amount") > 0) & F.col("application_date").isNotNull()

(apps.filter(is_valid).write.mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("silver.loan_applications"))

(apps.filter(~is_valid)
    .withColumn("_reason", F.when(F.col("loan_amount") <= 0, "non_positive_amount")
                            .otherwise("unparseable_date"))
    .write.mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable("quarantine.loan_applications"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ---------- CELL 6 : enable Change Data Feed (needed for incremental MLV refresh) ----------
for t in ["silver.customers", "silver.loan_applications"]:
    spark.sql(f"ALTER TABLE {t} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ---------- CELL 7 : reconcile counts (pipeline-friendly exit value) ----------
counts = {
    "raw_apps": spark.table(f"{src}.loan_applications").count(),
    "silver_apps": spark.table("silver.loan_applications").count(),
    "quarantined": spark.table("quarantine.loan_applications").count(),
    "silver_customers": spark.table("silver.customers").count(),
}
print(counts)
notebookutils.notebook.exit(str(counts))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Run in a notebook cell with %%sql  (default lakehouse: lh_silver)
# MAGIC CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS gold.product_risk
# MAGIC (
# MAGIC     CONSTRAINT known_city CHECK (city IS NOT NULL) ON MISMATCH DROP
# MAGIC )
# MAGIC COMMENT 'Approval and default rate by product and city'
# MAGIC AS
# MAGIC SELECT
# MAGIC     a.product,
# MAGIC     c.city,
# MAGIC     COUNT(*)                                                         AS applications,
# MAGIC     SUM(CASE WHEN a.status = 'Approved' THEN 1 ELSE 0 END)           AS approved_apps,
# MAGIC     SUM(CASE WHEN a.defaulted = 1 THEN 1 ELSE 0 END)                 AS defaults,
# MAGIC     ROUND(SUM(a.loan_amount), 2)                                     AS total_amount
# MAGIC FROM silver.loan_applications a
# MAGIC JOIN silver.customers c ON a.customer_id = c.customer_id
# MAGIC GROUP BY a.product, c.city;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
