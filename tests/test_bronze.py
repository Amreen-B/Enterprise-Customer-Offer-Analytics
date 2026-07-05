"""
============================================================
Bronze Layer Unit Tests
============================================================
"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Bronze Tests")
    .getOrCreate()
)


def test_bronze_table_exists():

    assert spark.catalog.tableExists(
        "workspace.default.bronze_customers"
    )


def test_bronze_not_empty():

    df = spark.table(
        "workspace.default.bronze_customers"
    )

    assert df.count() > 0


def test_ingestion_timestamp_exists():

    df = spark.table(
        "workspace.default.bronze_customers"
    )

    assert "ingestion_timestamp" in df.columns


def test_source_system_exists():

    df = spark.table(
        "workspace.default.bronze_customers"
    )

    assert "source_system" in df.columns