# ============================================================
# Notebook : 02 - Bronze ETL
# Layer    : Bronze
# Purpose  : Read raw customer data, perform basic validation,
#            add ingestion metadata, and create Bronze table.
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Bronze ETL") \
    .getOrCreate()

print("=" * 70)
print("BRONZE LAYER ETL STARTED")
print("=" * 70)

# ------------------------------------------------------------
# Read Raw Table
# ------------------------------------------------------------

bronze_df = spark.table("workspace.default.customers_raw")

print("\nRaw Table Loaded Successfully.")

# ------------------------------------------------------------
# Display Raw Data
# ------------------------------------------------------------

display(bronze_df)

# ------------------------------------------------------------
# Print Schema
# ------------------------------------------------------------

print("\nSchema")
print("-" * 70)

bronze_df.printSchema()

# ------------------------------------------------------------
# Dataset Information
# ------------------------------------------------------------

rows = bronze_df.count()
columns = len(bronze_df.columns)

print("\nDataset Information")
print("-" * 70)

print(f"Rows      : {rows}")
print(f"Columns   : {columns}")

# ------------------------------------------------------------
# Add Metadata Columns
# ------------------------------------------------------------

bronze_df = (
    bronze_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_system", lit("Bank Marketing Dataset"))
)

print("\nMetadata Columns Added")

# ------------------------------------------------------------
# Display Updated Data
# ------------------------------------------------------------

display(bronze_df)

# ------------------------------------------------------------
# Save Bronze Table
# ------------------------------------------------------------

bronze_df.write \
    .mode("overwrite") \
    .saveAsTable("workspace.default.bronze_customers")

print("\nBronze Table Created Successfully.")

# ------------------------------------------------------------
# Verify Bronze Table
# ------------------------------------------------------------

bronze_table = spark.table("workspace.default.bronze_customers")

display(bronze_table.limit(10))

# ------------------------------------------------------------
# Show Available Tables
# ------------------------------------------------------------

print("\nAvailable Tables")
print("-" * 70)

spark.sql("SHOW TABLES IN workspace.default").show(truncate=False)

# ------------------------------------------------------------
# Verify Bronze Table Exists
# ------------------------------------------------------------

if spark.catalog.tableExists("workspace.default.bronze_customers"):
    print("\nSUCCESS : Bronze table created.")
else:
    print("\nERROR : Bronze table creation failed.")

# ------------------------------------------------------------
# Record Count Validation
# ------------------------------------------------------------

bronze_count = bronze_table.count()

print("\nValidation")
print("-" * 70)

print(f"Raw Records      : {rows}")
print(f"Bronze Records   : {bronze_count}")

if rows == bronze_count:
    print("Record Validation : PASSED")
else:
    print("Record Validation : FAILED")

# ------------------------------------------------------------
# Notebook Summary
# ------------------------------------------------------------

print("\nSummary")
print("-" * 70)

print(f"""
Source Table      : workspace.default.customers_raw

Target Table      : workspace.default.bronze_customers

Rows Processed    : {bronze_count}

Metadata Added    :
    - ingestion_timestamp
    - source_system

Status            : SUCCESS

Next Notebook     : 03_Silver_ETL.py
""")

print("=" * 70)
print("BRONZE ETL COMPLETED")
print("=" * 70)