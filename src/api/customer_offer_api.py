from fastapi import FastAPI
from pyspark.sql import SparkSession

app = FastAPI(
    title="Enterprise Customer Offer Management API",
    version="1.0"
)

spark = (
    SparkSession.builder
    .appName("Customer API")
    .getOrCreate()
)


@app.get("/")
def home():

    return {
        "Project": "Enterprise Customer Offer Management",
        "Version": "1.0",
        "Author": "Amreen Begum"
    }


@app.get("/health")
def health():

    return {
        "status": "Healthy"
    }


@app.get("/gold/customer-summary")
def customer_summary():

    df = spark.table("workspace.default.gold_customer_summary")

    return df.limit(20).toPandas().to_dict(orient="records")


@app.get("/gold/product-summary")
def product_summary():

    df = spark.table("workspace.default.gold_product_summary")

    return df.limit(20).toPandas().to_dict(orient="records")


@app.get("/gold/transaction-summary")
def transaction_summary():

    df = spark.table("workspace.default.gold_transaction_summary")

    return df.limit(20).toPandas().to_dict(orient="records")


@app.get("/gold/offer-summary")
def offer_summary():

    df = spark.table("workspace.default.gold_offer_summary")

    return df.limit(20).toPandas().to_dict(orient="records")