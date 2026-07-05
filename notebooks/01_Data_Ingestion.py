# ============================================================
# Notebook : 01 - Data Ingestion
# Purpose  : Load raw CSV into Unity Catalog
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Customer Data Ingestion") \
    .getOrCreate()

print("=" * 70)
print("CUSTOMER DATA INGESTION")
print("=" * 70)

# ------------------------------------------------------------
# Read Raw Table
# ------------------------------------------------------------
# The CSV has already been uploaded and converted into a table
# named workspace.default.customers_raw
# ------------------------------------------------------------

customers_df = spark.table("workspace.default.customers_raw")

print("\nRaw Dataset Loaded Successfully.")

# ------------------------------------------------------------
# Display Dataset
# ------------------------------------------------------------

display(customers_df)

# ------------------------------------------------------------
# Verify Schema
# ------------------------------------------------------------

print("\nSchema")
print("-" * 70)

customers_df.printSchema()

# ------------------------------------------------------------
# Dataset Information
# ------------------------------------------------------------

rows = customers_df.count()
cols = len(customers_df.columns)

print("\nDataset Information")
print("-" * 70)
print(f"Rows       : {rows}")
print(f"Columns    : {cols}")

# ------------------------------------------------------------
# Check Available Tables
# ------------------------------------------------------------

print("\nTables Available")
print("-" * 70)

spark.sql("SHOW TABLES IN workspace.default").show(truncate=False)

# ------------------------------------------------------------
# Verify Table Exists
# ------------------------------------------------------------

print("\nVerifying customers_raw table...")

table_exists = spark.catalog.tableExists("workspace.default.customers_raw")

if table_exists:
    print("SUCCESS : customers_raw table found.")
else:
    print("ERROR : customers_raw table not found.")

# ------------------------------------------------------------
# Data Preview
# ------------------------------------------------------------

print("\nFirst Five Records")
print("-" * 70)

display(customers_df.limit(5))

# ------------------------------------------------------------
# Basic Data Validation
# ------------------------------------------------------------

print("\nChecking Empty Dataset")

if rows == 0:
    print("Dataset is empty.")
else:
    print("Dataset contains records.")

# ------------------------------------------------------------
# Column List
# ------------------------------------------------------------

print("\nColumns")
print("-" * 70)

for i, column in enumerate(customers_df.columns, start=1):
    print(f"{i}. {column}")

# ------------------------------------------------------------
# Notebook Summary
# ------------------------------------------------------------

print("\nSummary")
print("-" * 70)

print(f"""
Source             : customers_raw.csv

Target Table       : workspace.default.customers_raw

Rows Loaded        : {rows}

Columns Loaded     : {cols}

Status             : SUCCESS

Next Step          : Bronze ETL
""")

print("=" * 70)
print("DATA INGESTION COMPLETED")
print("=" * 70)