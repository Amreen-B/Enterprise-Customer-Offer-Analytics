"""
============================================================
Enterprise Data Engineering Project
Silver Pipeline
============================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

from utils.logger import get_logger
from utils.helpers import rename_special_columns
from utils.helpers import show_dataset_info

logger = get_logger(__name__)


def run():

    spark = (
        SparkSession.builder
        .appName("Silver Pipeline")
        .getOrCreate()
    )

    logger.info("Reading Bronze Table")

    df = spark.table("workspace.default.bronze_customers")

    df = rename_special_columns(df)

    window = Window.orderBy(monotonically_increasing_id())

    df = df.withColumn(
        "customer_id",
        row_number().over(window)
    )

    cols = ["customer_id"] + [
        c for c in df.columns
        if c != "customer_id"
    ]

    df = df.select(cols)

    df = df.dropDuplicates()

    show_dataset_info(df)

    df.write \
        .mode("overwrite") \
        .saveAsTable("workspace.default.silver_customers")

    logger.info("Silver Table Created")


if __name__ == "__main__":
    run()