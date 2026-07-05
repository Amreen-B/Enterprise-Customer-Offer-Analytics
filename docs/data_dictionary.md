# Data Dictionary

## Project Overview

This document describes the datasets used in the Enterprise Customer Offer Analytics Platform.

---

# 1. Customer Dataset

**File:** `customers_raw.csv`

| Column | Data Type | Description |
|---------|-----------|-------------|
| customer_id | Integer | Unique identifier for each customer |
| age | Integer | Customer age |
| gender | String | Customer gender |
| city | String | Customer city/location |

---

# 2. Offer Dataset

| Column | Data Type | Description |
|---------|-----------|-------------|
| customer_id | Integer | Customer identifier |
| offer_type | String | Type of offer sent to the customer |
| channel | String | Communication channel (Call, SMS, Email, WhatsApp) |
| accepted | Integer | Offer acceptance (1 = Accepted, 0 = Rejected) |

---

# 3. Transaction Dataset

| Column | Data Type | Description |
|---------|-----------|-------------|
| transaction_id | Integer | Unique transaction identifier |
| customer_id | Integer | Customer identifier |
| product | String | Purchased financial product |
| amount | Decimal | Transaction amount |
| transaction_date | Date | Transaction date |

---

# Gold Layer Summary Tables

The Gold layer contains aggregated business-ready datasets used for reporting.

| Table | Purpose |
|--------|----------|
| Customer_Summary | Customer KPIs |
| Offer_Summary | Offer metrics |
| Product_Summary | Product revenue analysis |
| Channel_Summary | Channel performance |
| Age_Summary | Age-wise customer analysis |
| Monthly_Transactions | Monthly revenue trend |
| Transaction_Summary | Overall transaction KPIs |