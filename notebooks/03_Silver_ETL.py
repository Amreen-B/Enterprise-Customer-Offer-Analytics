# ============================================================
# Notebook : 03 - Silver ETL
# Layer    : Silver
# Purpose  : Clean, standardize and enrich Bronze data
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Silver ETL") \
    .getOrCreate()

print("="*70)
print("SILVER LAYER ETL STARTED")
print("="*70)

# ------------------------------------------------------------
# Read Bronze Table
# ------------------------------------------------------------

bronze_df = spark.table("workspace.default.bronze_customers")

print("\nBronze Table Loaded Successfully.")

display(bronze_df)

# ------------------------------------------------------------
# Dataset Information
# ------------------------------------------------------------

rows = bronze_df.count()
cols = len(bronze_df.columns)

print("\nDataset Information")
print("-"*70)
print(f"Rows      : {rows}")
print(f"Columns   : {cols}")

# ------------------------------------------------------------
# Rename Columns
# ------------------------------------------------------------

silver_df = (
    bronze_df
    .withColumnRenamed("emp.var.rate", "emp_var_rate")
    .withColumnRenamed("cons.price.idx", "cons_price_idx")
    .withColumnRenamed("cons.conf.idx", "cons_conf_idx")
    .withColumnRenamed("nr.employed", "nr_employed")
)

print("\nSpecial Character Columns Renamed.")

# ------------------------------------------------------------
# Generate Customer ID
# ------------------------------------------------------------

window_spec = Window.orderBy(monotonically_increasing_id())

silver_df = silver_df.withColumn(
    "customer_id",
    row_number().over(window_spec)
)

print("Customer ID Generated.")

# ------------------------------------------------------------
# Move Customer ID to First Column
# ------------------------------------------------------------

columns = ["customer_id"] + [
    c for c in silver_df.columns
    if c != "customer_id"
]

silver_df = silver_df.select(columns)

# ------------------------------------------------------------
# Remove Duplicate Records
# ------------------------------------------------------------

duplicate_rows = silver_df.count() - silver_df.dropDuplicates().count()

print(f"\nDuplicate Rows Found : {duplicate_rows}")

silver_df = silver_df.dropDuplicates()

print("Duplicate Records Removed.")

# ------------------------------------------------------------
# Missing Value Check
# ------------------------------------------------------------

print("\nMissing Values")
print("-"*70)

missing_df = silver_df.select([
    count(
        when(col(c).isNull(), c)
    ).alias(c)
    for c in silver_df.columns
])

display(missing_df)

# ------------------------------------------------------------
# Summary Statistics
# ------------------------------------------------------------

print("\nSummary Statistics")
print("-"*70)

display(silver_df.describe())

# ------------------------------------------------------------
# Preview Clean Dataset
# ------------------------------------------------------------

display(silver_df.limit(20))

# ------------------------------------------------------------
# Save Silver Table
# ------------------------------------------------------------

silver_df.write \
    .mode("overwrite") \
    .saveAsTable("workspace.default.silver_customers")

print("\nSilver Table Created Successfully.")

# ------------------------------------------------------------
# Validate Saved Table
# ------------------------------------------------------------

silver_table = spark.table("workspace.default.silver_customers")

display(silver_table.limit(10))

# ------------------------------------------------------------
# Row Count Validation
# ------------------------------------------------------------

silver_rows = silver_table.count()

print("\nValidation")
print("-"*70)

print(f"Bronze Rows : {rows}")
print(f"Silver Rows : {silver_rows}")

# ------------------------------------------------------------
# Show Tables
# ------------------------------------------------------------

spark.sql(
    "SHOW TABLES IN workspace.default"
).show(truncate=False)

# ------------------------------------------------------------
# Schema
# ------------------------------------------------------------

print("\nSilver Schema")
print("-"*70)

silver_table.printSchema()

# ------------------------------------------------------------
# Notebook Summary
# ------------------------------------------------------------

print("\nSummary")
print("-"*70)

print(f"""
Source Table      : bronze_customers

Target Table      : silver_customers

Rows Processed    : {silver_rows}

Transformations

✔ Renamed columns

✔ Generated Customer ID

✔ Removed duplicates

✔ Checked missing values

✔ Standardized schema

Status            : SUCCESS

Next Notebook     : 04_Data_Quality.py
""")

print("="*70)
print("SILVER ETL COMPLETED")
print("="*70)