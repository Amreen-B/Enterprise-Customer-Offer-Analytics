"""
============================================================
Gold Layer Unit Tests
============================================================
"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Gold Tests")
    .getOrCreate()
)


gold_tables = [

    "gold_customer_summary",

    "gold_transaction_summary",

    "gold_product_summary",

    "gold_offer_summary",

    "gold_channel_summary",

    "gold_age_summary",

    "gold_monthly_transactions"

]


def test_gold_tables_exist():

    for table in gold_tables:

        assert spark.catalog.tableExists(
            f"workspace.default.{table}"
        )


def test_gold_tables_not_empty():

    for table in gold_tables:

        df = spark.table(
            f"workspace.default.{table}"
        )

        assert df.count() > 0