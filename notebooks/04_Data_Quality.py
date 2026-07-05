# ============================================================
# Notebook : 04 - Data Quality
# Layer    : Validation Framework
# Purpose  : Perform data quality validation on Silver Layer
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Data Quality Framework") \
    .getOrCreate()

print("=" * 80)
print("DATA QUALITY VALIDATION STARTED")
print("=" * 80)

# ------------------------------------------------------------
# Read Silver Table
# ------------------------------------------------------------

df = spark.table("workspace.default.silver_customers")

display(df)

# ------------------------------------------------------------
# Dataset Information
# ------------------------------------------------------------

rows = df.count()
cols = len(df.columns)

print("\nDataset Information")
print("-" * 80)
print(f"Rows    : {rows}")
print(f"Columns : {cols}")

# ------------------------------------------------------------
# 1. Missing Value Check
# ------------------------------------------------------------

print("\n1. Missing Value Validation")
print("-" * 80)

missing_df = df.select([
    count(
        when(col(c).isNull(), c)
    ).alias(c)
    for c in df.columns
])

display(missing_df)

# ------------------------------------------------------------
# 2. Duplicate Record Validation
# ------------------------------------------------------------

print("\n2. Duplicate Validation")
print("-" * 80)

duplicate_count = rows - df.dropDuplicates().count()

print(f"Duplicate Records : {duplicate_count}")

# ------------------------------------------------------------
# 3. Data Type Validation
# ------------------------------------------------------------

print("\n3. Data Type Validation")
print("-" * 80)

df.printSchema()

# ------------------------------------------------------------
# 4. Customer ID Validation
# ------------------------------------------------------------

print("\n4. Customer ID Validation")
print("-" * 80)

null_customer_id = df.filter(
    col("customer_id").isNull()
).count()

duplicate_customer_id = (
    df.groupBy("customer_id")
      .count()
      .filter(col("count") > 1)
      .count()
)

print(f"Null Customer IDs      : {null_customer_id}")
print(f"Duplicate Customer IDs : {duplicate_customer_id}")

# ------------------------------------------------------------
# 5. Age Validation
# ------------------------------------------------------------

print("\n5. Age Validation")
print("-" * 80)

invalid_age = df.filter(
    (col("age") < 18) |
    (col("age") > 100)
).count()

print(f"Invalid Age Records : {invalid_age}")

# ------------------------------------------------------------
# 6. Campaign Validation
# ------------------------------------------------------------

print("\n6. Campaign Validation")
print("-" * 80)

invalid_campaign = df.filter(
    col("campaign") <= 0
).count()

print(f"Invalid Campaign Records : {invalid_campaign}")

# ------------------------------------------------------------
# 7. Duration Validation
# ------------------------------------------------------------

print("\n7. Duration Validation")
print("-" * 80)

invalid_duration = df.filter(
    col("duration") < 0
).count()

print(f"Invalid Duration Records : {invalid_duration}")

# ------------------------------------------------------------
# 8. Numeric Summary
# ------------------------------------------------------------

print("\n8. Numeric Statistics")
print("-" * 80)

display(df.describe())

# ------------------------------------------------------------
# 9. Distinct Value Analysis
# ------------------------------------------------------------

categorical_columns = [
    "job",
    "education",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
    "y"
]

print("\n9. Distinct Value Counts")
print("-" * 80)

for column in categorical_columns:

    count_values = df.select(column).distinct().count()

    print(f"{column:<20} {count_values}")

# ------------------------------------------------------------
# 10. Data Quality Score
# ------------------------------------------------------------

print("\n10. Data Quality Score")
print("-" * 80)

checks = {
    "Null Customer ID": null_customer_id == 0,
    "Duplicate Customer ID": duplicate_customer_id == 0,
    "Duplicate Records": duplicate_count == 0,
    "Invalid Age": invalid_age == 0,
    "Invalid Campaign": invalid_campaign == 0,
    "Invalid Duration": invalid_duration == 0
}

passed = sum(checks.values())
total = len(checks)

score = round((passed / total) * 100, 2)

print(f"Quality Score : {score}%")

# ------------------------------------------------------------
# Data Quality Report
# ------------------------------------------------------------

print("\nData Quality Report")
print("-" * 80)

for rule, status in checks.items():

    print(f"{rule:<30} {'PASS' if status else 'FAIL'}")

# ------------------------------------------------------------
# Notebook Summary
# ------------------------------------------------------------

print("\nSummary")
print("-" * 80)

print(f"""
Source Table      : silver_customers

Rows Validated    : {rows}

Columns           : {cols}

Validation Rules

✔ Missing Values

✔ Duplicate Records

✔ Customer ID

✔ Age Validation

✔ Campaign Validation

✔ Duration Validation

Overall Quality Score : {score} %

Status : SUCCESS
""")

print("=" * 80)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 80)