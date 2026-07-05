# ============================================================
# Notebook : 07 - Query Optimization
# Layer    : Performance Optimization
# Purpose  : Demonstrate Spark optimization techniques
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import broadcast
import time

# ------------------------------------------------------------
# Create Spark Session
# ------------------------------------------------------------

spark = SparkSession.builder \
    .appName("Query Optimization") \
    .getOrCreate()

print("=" * 80)
print("QUERY OPTIMIZATION")
print("=" * 80)

# ------------------------------------------------------------
# Load Tables
# ------------------------------------------------------------

customers = spark.table("workspace.default.silver_customers")
transactions = spark.table("workspace.default.transactions")
offers = spark.table("workspace.default.offers")

# ------------------------------------------------------------
# Dataset Information
# ------------------------------------------------------------

print("\nDataset Information")
print("-" * 80)

print(f"Customers    : {customers.count()}")
print(f"Transactions : {transactions.count()}")
print(f"Offers       : {offers.count()}")

# ============================================================
# 1. Explain Execution Plan
# ============================================================

print("\nExecution Plan")
print("-" * 80)

customers.explain(True)

# ============================================================
# 2. Cache DataFrame
# ============================================================

print("\nCaching Customers Table")

customers.cache()

customers.count()

print("Customers table cached successfully.")

# ============================================================
# 3. Persist DataFrame
# ============================================================

print("\nPersisting Transactions Table")

transactions.persist()

transactions.count()

print("Transactions table persisted successfully.")

# ============================================================
# 4. Repartition
# ============================================================

print("\nRepartitioning Transactions")

transactions_repartitioned = transactions.repartition(4)

print("Number of Partitions:",
      transactions_repartitioned.rdd.getNumPartitions())

# ============================================================
# 5. Broadcast Join
# ============================================================

print("\nBroadcast Join")

broadcast_join = transactions.join(
    broadcast(customers),
    "customer_id"
)

display(broadcast_join.limit(10))

# ============================================================
# 6. Normal Join Performance
# ============================================================

print("\nNormal Join Performance")

start = time.time()

normal_join = transactions.join(
    customers,
    "customer_id"
)

normal_join.count()

normal_time = time.time() - start

print(f"Normal Join Time : {round(normal_time,2)} seconds")

# ============================================================
# 7. Broadcast Join Performance
# ============================================================

print("\nBroadcast Join Performance")

start = time.time()

optimized_join = transactions.join(
    broadcast(customers),
    "customer_id"
)

optimized_join.count()

optimized_time = time.time() - start

print(f"Broadcast Join Time : {round(optimized_time,2)} seconds")

# ============================================================
# 8. Aggregation Performance
# ============================================================

print("\nAggregation")

product_summary = (
    transactions
    .groupBy("product")
    .agg(
        count("*").alias("Transactions"),
        round(sum("amount"),2).alias("Revenue")
    )
)

display(product_summary)

# ============================================================
# 9. Explain Optimized Query
# ============================================================

print("\nOptimized Execution Plan")

optimized_join.explain(True)

# ============================================================
# 10. Performance Report
# ============================================================

print("\nPerformance Report")
print("-" * 80)

print(f"""
Normal Join Time      : {round(normal_time,2)} sec

Broadcast Join Time   : {round(optimized_time,2)} sec

Improvement           : {round(((normal_time-optimized_time)/normal_time)*100,2)} %

Optimization Techniques

✔ DataFrame Cache

✔ Persist

✔ Repartition

✔ Broadcast Join

✔ Explain Plan

✔ Aggregation Optimization
""")

print("=" * 80)
print("QUERY OPTIMIZATION COMPLETED")
print("=" * 80)