# Project Workflow

## Overview

The Enterprise Customer Offer Analytics Platform follows the **Medallion Architecture (Bronze, Silver, Gold)** to transform raw customer and transaction data into business-ready datasets for reporting and analytics.

---

# Workflow Diagram

```text
                Raw CSV Files
                     │
                     ▼
             Data Profiling
                     │
                     ▼
            Data Ingestion
                     │
                     ▼
        Bronze Layer (Raw Data)
                     │
                     ▼
 Silver Layer (Cleaned & Validated Data)
                     │
                     ▼
 Gold Layer (Business Aggregations)
                     │
                     ▼
          SQL Business Analytics
                     │
                     ▼
         Export Gold Tables (CSV)
                     │
                     ▼
         Power BI Interactive Dashboard
```

---

# Step 1 – Data Profiling

**Script:** `00_data_profiling.py`

Purpose:

- Analyze raw datasets
- Check missing values
- Review data types
- Identify duplicate records
- Generate initial data quality insights

---

# Step 2 – Data Ingestion

**Script:** `01_Data_Ingestion.py`

Purpose:

- Read raw CSV files
- Load datasets into Databricks
- Validate schema
- Store raw data for downstream processing

---

# Step 3 – Bronze Layer

**Script:** `src/pipelines/bronze.py`

Purpose:

- Store raw datasets without business transformations
- Preserve original data for traceability
- Create Bronze Delta tables

---

# Step 4 – Silver Layer

**Script:** `src/pipelines/silver.py`

Purpose:

- Remove duplicate records
- Handle missing values
- Standardize column names
- Validate data quality
- Apply business rules

---

# Step 5 – Data Quality Validation

**Scripts:**
- `04_Data_Quality.py`
- `src/utils/validation.py`

Purpose:

- Validate cleaned datasets
- Check null values
- Verify data consistency
- Ensure business rules are satisfied

---

# Step 6 – Gold Layer

**Script:** `src/pipelines/gold.py`

Purpose:

Generate business-ready summary tables:

- Customer Summary
- Offer Summary
- Product Summary
- Channel Summary
- Age Group Summary
- Monthly Transaction Summary
- Transaction Summary

These tables are optimized for reporting and dashboard development.

---

# Step 7 – SQL Analytics

**Script:** `sql/business_queries.sql`

Purpose:

Perform business analysis such as:

- Offer acceptance analysis
- Revenue analysis
- Customer segmentation
- Channel performance
- Product performance

---

# Step 8 – Export for Power BI

**Script:** `src/pipelines/powerbi_export.py`

Purpose:

- Export Gold tables as CSV files
- Prepare datasets for Power BI
- Ensure reporting-ready data

---

# Step 9 – Power BI Dashboard

Power BI consumes the exported Gold datasets to create two interactive dashboards:

## Executive Dashboard

Provides:

- Total Customers
- Average Age
- Offers Sent
- Total Transactions
- Revenue by Product
- Monthly Revenue Trend

---

## Customer Insights Dashboard

Provides:

- Offer Distribution
- Acceptance Rate by Channel
- Offer Acceptance by Age Group
- Age Group Summary Matrix
- Interactive slicers for Offer Type, Age Group, and Channel

---

# Technologies Used

- Python
- PySpark
- Databricks
- SQL
- Delta Lake
- Power BI
- Git & GitHub

---

# Outcome

The pipeline transforms raw enterprise banking data into clean, aggregated datasets that enable interactive business intelligence reporting and support data-driven decision-making.