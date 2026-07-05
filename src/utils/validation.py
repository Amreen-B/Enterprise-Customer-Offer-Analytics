"""
============================================================
File : validation.py
Purpose : Data validation utilities
============================================================
"""

from pyspark.sql.functions import *


def row_count(df):

    return df.count()


def duplicate_count(df):

    return df.count() - df.dropDuplicates().count()


def missing_values(df):

    return df.select(

        [

            count(

                when(col(c).isNull(), c)

            ).alias(c)

            for c in df.columns

        ]

    )


def table_exists(spark, table_name):

    return spark.catalog.tableExists(table_name)


def print_schema(df):

    df.printSchema()