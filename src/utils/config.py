"""
============================================================
File : config.py
Purpose : Central configuration file
============================================================
"""

# -------------------------------
# Project Information
# -------------------------------

PROJECT_NAME = "Enterprise Customer Offer Management"

VERSION = "1.0"

AUTHOR = "Amreen Begum"

# -------------------------------
# Dataset Paths
# -------------------------------

RAW_DATA_PATH = "datasets/customers_raw.csv"

# -------------------------------
# Bronze Layer
# -------------------------------

BRONZE_TABLE = "workspace.default.bronze_customers"

# -------------------------------
# Silver Layer
# -------------------------------

SILVER_TABLE = "workspace.default.silver_customers"

# -------------------------------
# Business Tables
# -------------------------------

TRANSACTION_TABLE = "workspace.default.transactions"

OFFER_TABLE = "workspace.default.offers"

# -------------------------------
# Gold Tables
# -------------------------------

GOLD_CUSTOMER = "workspace.default.gold_customer_summary"

GOLD_TRANSACTION = "workspace.default.gold_transaction_summary"

GOLD_PRODUCT = "workspace.default.gold_product_summary"

GOLD_OFFER = "workspace.default.gold_offer_summary"

GOLD_CHANNEL = "workspace.default.gold_channel_summary"

GOLD_AGE = "workspace.default.gold_age_summary"

GOLD_MONTHLY = "workspace.default.gold_monthly_transactions"

# -------------------------------
# Metadata
# -------------------------------

SOURCE_SYSTEM = "Bank Marketing Dataset"

INGESTION_MODE = "Overwrite"
