# ============================================================
# Notebook: 00 - Data Profiling
# Purpose : Explore and understand raw customer dataset
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Customer Data Profiling") \
    .getOrCreate()

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

df = spark.table("workspace.default.customers_raw")

print("="*70)
print("CUSTOMER DATASET LOADED")
print("="*70)

# ------------------------------------------------------------
# Display Dataset
# ------------------------------------------------------------

display(df)

# ------------------------------------------------------------
# Print Schema
# ------------------------------------------------------------

print("\nSchema")
print("-"*70)

df.printSchema()

# ------------------------------------------------------------
# Dataset Size
# ------------------------------------------------------------

rows = df.count()
columns = len(df.columns)

print("\nDataset Information")
print("-"*70)
print(f"Rows    : {rows}")
print(f"Columns : {columns}")

# ------------------------------------------------------------
# Column Names
# ------------------------------------------------------------

print("\nColumn Names")
print("-"*70)

for i, col_name in enumerate(df.columns, start=1):
    print(f"{i}. {col_name}")

# ------------------------------------------------------------
# Summary Statistics
# ------------------------------------------------------------

print("\nSummary Statistics")
print("-"*70)

display(df.describe())

# ------------------------------------------------------------
# Missing Values
# ------------------------------------------------------------

print("\nMissing Values")
print("-"*70)

missing_df = df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
])

display(missing_df)

# ------------------------------------------------------------
# Duplicate Records
# ------------------------------------------------------------

duplicate_rows = df.count() - df.dropDuplicates().count()

print("\nDuplicate Rows")
print("-"*70)
print(f"Duplicate Records : {duplicate_rows}")

# ------------------------------------------------------------
# Data Types
# ------------------------------------------------------------

print("\nData Types")
print("-"*70)

for column_name, dtype in df.dtypes:
    print(f"{column_name:<25} {dtype}")

# ------------------------------------------------------------
# Distinct Values for Categorical Columns
# ------------------------------------------------------------

categorical_columns = [
    "job",
    "marital",
    "education",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
    "y"
]

print("\nUnique Value Counts")
print("-"*70)

for column in categorical_columns:
    unique_count = df.select(column).distinct().count()
    print(f"{column:<20} {unique_count}")

# ------------------------------------------------------------
# Sample Records
# ------------------------------------------------------------

print("\nSample Records")
print("-"*70)

display(df.limit(10))

# ------------------------------------------------------------
# Observations
# ------------------------------------------------------------

print("\nObservations")
print("-"*70)

print("""
1. Dataset contains customer marketing campaign data.

2. Total records are suitable for big data processing.

3. No missing values detected.

4. Duplicate records exist and will be removed in Silver Layer.

5. Column names contain '.' characters and will be renamed.

6. Customer ID is not available and will be generated.

7. Dataset will follow Medallion Architecture:
   Raw -> Bronze -> Silver -> Gold
""")

print("="*70)
print("DATA PROFILING COMPLETED")
print("="*70)