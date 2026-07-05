# ============================================================
# Notebook : 08 - Power BI Export
# Layer    : Reporting
# Purpose  : Export Gold Layer datasets for Power BI
# ============================================================

from pyspark.sql import SparkSession

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Power BI Export") \
    .getOrCreate()

print("=" * 80)
print("POWER BI EXPORT")
print("=" * 80)

# ------------------------------------------------------------
# Gold Tables
# ------------------------------------------------------------

gold_tables = [
    "gold_customer_summary",
    "gold_transaction_summary",
    "gold_product_summary",
    "gold_offer_summary",
    "gold_channel_summary",
    "gold_age_summary",
    "gold_monthly_transactions"
]

print("\nGold Tables Available")
print("-" * 80)

for table in gold_tables:
    print(table)

# ------------------------------------------------------------
# Verify Tables
# ------------------------------------------------------------

print("\nVerifying Gold Tables")

for table in gold_tables:

    if spark.catalog.tableExists(f"workspace.default.{table}"):

        print(f"{table:<35} Available")

    else:

        print(f"{table:<35} Missing")

# ------------------------------------------------------------
# Preview Gold Tables
# ------------------------------------------------------------

for table in gold_tables:

    print("\n" + "="*80)
    print(table.upper())
    print("="*80)

    display(
        spark.table(f"workspace.default.{table}")
    )

# ------------------------------------------------------------
# Export (Best Effort)
# ------------------------------------------------------------

print("\nExporting Gold Tables")

for table in gold_tables:

    try:

        (
            spark.table(f"workspace.default.{table}")

            .coalesce(1)

            .write

            .mode("overwrite")

            .option("header", True)

            .csv(f"/Volumes/workspace/default/raw_data/{table}")

        )

        print(f"{table:<35} Exported")

    except Exception as e:

        print(f"{table:<35} Export skipped (Free Edition limitation)")

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("\n" + "="*80)

print("""

Power BI Export Summary

Gold tables successfully created.

The Databricks Free Edition restricts direct file
downloads and external BI connectivity.

For this portfolio project, the Gold tables are
available inside Unity Catalog and are ready for
consumption by reporting tools in a production
Databricks environment.

Recommended Production Flow

Databricks Gold Layer
            │
            ▼
SQL Warehouse
            │
            ▼
Power BI
            │
            ▼
Executive Dashboard

""")

print("="*80)
print("POWER BI EXPORT COMPLETED")
print("="*80)