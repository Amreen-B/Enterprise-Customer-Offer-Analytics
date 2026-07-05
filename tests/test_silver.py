"""
============================================================
Silver Layer Unit Tests
============================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("Silver Tests")
    .getOrCreate()
)


def test_silver_exists():

    assert spark.catalog.tableExists(
        "workspace.default.silver_customers"
    )


def test_customer_id_exists():

    df = spark.table(
        "workspace.default.silver_customers"
    )

    assert "customer_id" in df.columns


def test_customer_id_unique():

    df = spark.table(
        "workspace.default.silver_customers"
    )

    total = df.count()

    unique = df.select(
        "customer_id"
    ).distinct().count()

    assert total == unique


def test_no_duplicate_rows():

    df = spark.table(
        "workspace.default.silver_customers"
    )

    duplicates = df.count() - df.dropDuplicates().count()

    assert duplicates == 0