# ============================================================
# Notebook : 05 - Gold ETL
# Layer    : Gold
# Purpose  : Build business-ready analytical tables
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Gold ETL") \
    .getOrCreate()

print("=" * 80)
print("GOLD LAYER ETL STARTED")
print("=" * 80)

# ------------------------------------------------------------
# Read Silver & Business Tables
# ------------------------------------------------------------

customers = spark.table("workspace.default.silver_customers")
transactions = spark.table("workspace.default.transactions")
offers = spark.table("workspace.default.offers")

print("Tables Loaded Successfully.")

# ------------------------------------------------------------
# Customer Summary
# ------------------------------------------------------------

gold_customer_summary = (
    customers
    .groupBy("job", "education", "marital")
    .agg(
        count("*").alias("total_customers"),
        avg("age").alias("average_age")
    )
)

# ------------------------------------------------------------
# Transaction Summary
# ------------------------------------------------------------

gold_transaction_summary = (
    transactions
    .groupBy("status")
    .agg(
        count("*").alias("total_transactions"),
        round(sum("amount"),2).alias("total_amount"),
        round(avg("amount"),2).alias("average_amount")
    )
)

# ------------------------------------------------------------
# Product Performance
# ------------------------------------------------------------

gold_product_summary = (
    transactions
    .groupBy("product")
    .agg(
        count("*").alias("transactions"),
        round(sum("amount"),2).alias("revenue")
    )
    .orderBy(desc("revenue"))
)

# ------------------------------------------------------------
# Offer Performance
# ------------------------------------------------------------

gold_offer_summary = (
    offers
    .groupBy("offer_type")
    .agg(
        count("*").alias("offers_sent"),
        sum(
            when(col("accepted")=="Yes",1).otherwise(0)
        ).alias("accepted")
    )
)

gold_offer_summary = gold_offer_summary.withColumn(
    "acceptance_rate",
    round(
        col("accepted") /
        col("offers_sent") * 100,
        2
    )
)

# ------------------------------------------------------------
# Channel Performance
# ------------------------------------------------------------

gold_channel_summary = (
    offers
    .groupBy("channel")
    .agg(
        count("*").alias("offers"),
        sum(
            when(col("accepted")=="Yes",1).otherwise(0)
        ).alias("accepted")
    )
)

gold_channel_summary = gold_channel_summary.withColumn(
    "acceptance_rate",
    round(
        col("accepted") /
        col("offers") * 100,
        2
    )
)

# ------------------------------------------------------------
# Customer Age Group
# ------------------------------------------------------------

customer_offer = customers.join(
    offers,
    "customer_id"
)

customer_offer = customer_offer.withColumn(
    "age_group",
    when(col("age") < 30, "18-29")
    .when(col("age") < 45, "30-44")
    .when(col("age") < 60, "45-59")
    .otherwise("60+")
)

gold_age_summary = (
    customer_offer
    .groupBy("age_group")
    .agg(
        count("*").alias("offers"),
        sum(
            when(col("accepted")=="Yes",1).otherwise(0)
        ).alias("accepted")
    )
)

gold_age_summary = gold_age_summary.withColumn(
    "acceptance_rate",
    round(
        col("accepted") /
        col("offers") * 100,
        2
    )
)

# ------------------------------------------------------------
# Monthly Revenue
# ------------------------------------------------------------

gold_monthly_transactions = (
    transactions
    .withColumn(
        "month",
        date_format("transaction_date","MMM")
    )
    .groupBy("month")
    .agg(
        round(sum("amount"),2).alias("revenue")
    )
)

# ------------------------------------------------------------
# Display Results
# ------------------------------------------------------------

display(gold_customer_summary)
display(gold_transaction_summary)
display(gold_product_summary)
display(gold_offer_summary)
display(gold_channel_summary)
display(gold_age_summary)
display(gold_monthly_transactions)

# ------------------------------------------------------------
# Save Gold Tables
# ------------------------------------------------------------

gold_customer_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_customer_summary"
)

gold_transaction_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_transaction_summary"
)

gold_product_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_product_summary"
)

gold_offer_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_offer_summary"
)

gold_channel_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_channel_summary"
)

gold_age_summary.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_age_summary"
)

gold_monthly_transactions.write.mode("overwrite").saveAsTable(
    "workspace.default.gold_monthly_transactions"
)

# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

print("\nGold Tables Created Successfully.\n")

spark.sql(
    "SHOW TABLES IN workspace.default"
).show(truncate=False)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("=" * 80)
print("GOLD LAYER CREATED SUCCESSFULLY")
print("=" * 80)

print("""

Business Tables Created

✔ gold_customer_summary

✔ gold_transaction_summary

✔ gold_product_summary

✔ gold_offer_summary

✔ gold_channel_summary

✔ gold_age_summary

✔ gold_monthly_transactions

Status : SUCCESS

Next Notebook : 06_SQL_Analytics.sql

""")