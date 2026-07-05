"""
============================================================
Bronze Pipeline
============================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

from utils.logger import get_logger
from utils.helpers import show_dataset_info
from utils.validation import table_exists

logger = get_logger(__name__)


def run():

    spark = (
        SparkSession.builder
        .appName("Bronze Pipeline")
        .getOrCreate()
    )

    logger.info("Reading Raw Table...")

    bronze_df = spark.table("workspace.default.customers_raw")

    bronze_df = (
        bronze_df
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_system", lit("Bank Marketing Dataset"))
    )

    show_dataset_info(bronze_df)

    bronze_df.write \
        .mode("overwrite") \
        .saveAsTable("workspace.default.bronze_customers")

    if table_exists(spark, "workspace.default.bronze_customers"):
        logger.info("Bronze Table Created Successfully")


if __name__ == "__main__":
    run()