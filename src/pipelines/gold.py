"""
============================================================
Gold Pipeline
============================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from utils.logger import get_logger

logger = get_logger(__name__)


def run():

    spark = (
        SparkSession.builder
        .appName("Gold Pipeline")
        .getOrCreate()
    )

    customers = spark.table("workspace.default.silver_customers")
    transactions = spark.table("workspace.default.transactions")
    offers = spark.table("workspace.default.offers")

    logger.info("Creating Gold Tables")

    customer_summary = (
        customers
        .groupBy("job")
        .agg(count("*").alias("customers"))
    )

    product_summary = (
        transactions
        .groupBy("product")
        .agg(sum("amount").alias("revenue"))
    )

    offer_summary = (
        offers
        .groupBy("offer_type")
        .agg(count("*").alias("offers"))
    )

    customer_summary.write.mode("overwrite").saveAsTable(
        "workspace.default.gold_customer_summary"
    )

    product_summary.write.mode("overwrite").saveAsTable(
        "workspace.default.gold_product_summary"
    )

    offer_summary.write.mode("overwrite").saveAsTable(
        "workspace.default.gold_offer_summary"
    )

    logger.info("Gold Layer Created")


if __name__ == "__main__":
    run()