"""
============================================================
Export Pipeline
============================================================
"""

from pyspark.sql import SparkSession

from utils.logger import get_logger

logger = get_logger(__name__)


def export_table(spark, table_name, output_path):

    (
        spark.table(table_name)
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(output_path)
    )


def run():

    spark = (
        SparkSession.builder
        .appName("Export Pipeline")
        .getOrCreate()
    )

    tables = [

        "workspace.default.gold_customer_summary",

        "workspace.default.gold_transaction_summary",

        "workspace.default.gold_product_summary",

        "workspace.default.gold_offer_summary",

        "workspace.default.gold_channel_summary",

        "workspace.default.gold_age_summary",

        "workspace.default.gold_monthly_transactions"

    ]

    for table in tables:

        output = table.split(".")[-1]

        logger.info(f"Exporting {output}")

        try:

            export_table(
                spark,
                table,
                f"exports/{output}"
            )

        except Exception as e:

            logger.error(str(e))


if __name__ == "__main__":
    run()