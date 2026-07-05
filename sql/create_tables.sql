-- ============================================================
-- Create Tables Script
-- Purpose: Verify and document all Medallion tables
-- ============================================================

USE CATALOG workspace;
USE SCHEMA default;

-- ============================================================
-- Bronze Layer
-- ============================================================

-- Raw Customer Data
DESCRIBE TABLE customers_raw;

-- Bronze Customer Table
DESCRIBE TABLE bronze_customers;

-- ============================================================
-- Silver Layer
-- ============================================================

DESCRIBE TABLE silver_customers;

DESCRIBE TABLE transactions;

DESCRIBE TABLE offers;

-- ============================================================
-- Gold Layer
-- ============================================================

DESCRIBE TABLE gold_customer_summary;

DESCRIBE TABLE gold_transaction_summary;

DESCRIBE TABLE gold_product_summary;

DESCRIBE TABLE gold_offer_summary;

DESCRIBE TABLE gold_channel_summary;

DESCRIBE TABLE gold_age_summary;

DESCRIBE TABLE gold_monthly_transactions;

-- ============================================================
-- Verify Record Counts
-- ============================================================

SELECT 'customers_raw' AS table_name, COUNT(*) AS total_rows
FROM customers_raw

UNION ALL

SELECT 'bronze_customers', COUNT(*)
FROM bronze_customers

UNION ALL

SELECT 'silver_customers', COUNT(*)
FROM silver_customers

UNION ALL

SELECT 'transactions', COUNT(*)
FROM transactions

UNION ALL

SELECT 'offers', COUNT(*)
FROM offers;

-- ============================================================
-- List All Tables
-- ============================================================

SHOW TABLES;

-- ============================================================
-- End
-- ============================================================