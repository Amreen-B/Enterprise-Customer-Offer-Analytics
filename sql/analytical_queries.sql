-- ============================================================
-- Business Analytical Queries
-- ============================================================

USE CATALOG workspace;
USE SCHEMA default;

-- ============================================================
-- 1. Total Customers
-- ============================================================

SELECT COUNT(*) AS Total_Customers
FROM silver_customers;

-- ============================================================
-- 2. Customers by Job
-- ============================================================

SELECT
    job,
    COUNT(*) AS Total_Customers
FROM silver_customers
GROUP BY job
ORDER BY Total_Customers DESC;

-- ============================================================
-- 3. Customers by Marital Status
-- ============================================================

SELECT
    marital,
    COUNT(*) AS Total_Customers
FROM silver_customers
GROUP BY marital
ORDER BY Total_Customers DESC;

-- ============================================================
-- 4. Customers by Education
-- ============================================================

SELECT
    education,
    COUNT(*) AS Total_Customers
FROM silver_customers
GROUP BY education
ORDER BY Total_Customers DESC;

-- ============================================================
-- 5. Product Revenue
-- ============================================================

SELECT
    product,
    SUM(amount) AS Revenue
FROM transactions
GROUP BY product
ORDER BY Revenue DESC;

-- ============================================================
-- 6. Offer Acceptance Rate
-- ============================================================

SELECT
    accepted,
    COUNT(*) AS Customers
FROM offers
GROUP BY accepted;

-- ============================================================
-- 7. Marketing Channel Performance
-- ============================================================

SELECT
    channel,
    COUNT(*) AS Offers_Sent,
    SUM(CASE WHEN accepted='Yes' THEN 1 ELSE 0 END) AS Accepted
FROM offers
GROUP BY channel
ORDER BY Accepted DESC;

-- ============================================================
-- 8. Monthly Revenue
-- ============================================================

SELECT
    month,
    SUM(amount) AS Revenue
FROM transactions
GROUP BY month
ORDER BY Revenue DESC;

-- ============================================================
-- 9. Top 10 Customers by Spending
-- ============================================================

SELECT
    customer_id,
    SUM(amount) AS Total_Spent
FROM transactions
GROUP BY customer_id
ORDER BY Total_Spent DESC
LIMIT 10;

-- ============================================================
-- 10. Gold Customer Summary
-- ============================================================

SELECT *
FROM gold_customer_summary
ORDER BY Total_Customers DESC;

-- ============================================================
-- 11. Gold Product Summary
-- ============================================================

SELECT *
FROM gold_product_summary
ORDER BY Revenue DESC;

-- ============================================================
-- 12. Gold Offer Summary
-- ============================================================

SELECT *
FROM gold_offer_summary;

-- ============================================================
-- 13. Gold Channel Summary
-- ============================================================

SELECT *
FROM gold_channel_summary;

-- ============================================================
-- 14. Gold Monthly Transactions
-- ============================================================

SELECT *
FROM gold_monthly_transactions;

-- ============================================================
-- END
-- ============================================================