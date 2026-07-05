"""
============================================================
File : helpers.py
Purpose : Helper functions
============================================================
"""

from pyspark.sql.functions import *


def rename_special_columns(df):

    return (

        df

        .withColumnRenamed(

            "emp.var.rate",

            "emp_var_rate"

        )

        .withColumnRenamed(

            "cons.price.idx",

            "cons_price_idx"

        )

        .withColumnRenamed(

            "cons.conf.idx",

            "cons_conf_idx"

        )

        .withColumnRenamed(

            "nr.employed",

            "nr_employed"

        )

    )


def add_ingestion_timestamp(df):

    return df.withColumn(

        "ingestion_timestamp",

        current_timestamp()

    )


def show_dataset_info(df):

    print(f"Rows : {df.count()}")

    print(f"Columns : {len(df.columns)}")