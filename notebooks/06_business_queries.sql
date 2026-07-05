-- ============================================================
-- Notebook : 06 - SQL Analytics
-- Purpose  : Business Analytics using Spark SQL
-- ============================================================

---------------------------------------------------------------
-- 1. Total Customers
---------------------------------------------------------------

SELECT COUNT(*) AS total_customers
FROM workspace.default.silver_customers;

---------------------------------------------------------------
-- 2. Average Customer Age
---------------------------------------------------------------

SELECT ROUND(AVG(age),2) AS average_age
FROM workspace.default.silver_customers;

---------------------------------------------------------------
-- 3. Customers by Job
---------------------------------------------------------------

SELECT
    job,
    COUNT(*) AS total_customers
FROM workspace.default.silver_customers
GROUP BY job
ORDER BY total_customers DESC;

---------------------------------------------------------------
-- 4. Customers by Education
---------------------------------------------------------------

SELECT
    education,
    COUNT(*) AS total_customers
FROM workspace.default.silver_customers
GROUP BY education
ORDER BY total_customers DESC;

---------------------------------------------------------------
-- 5. Customers by Marital Status
---------------------------------------------------------------

SELECT
    marital,
    COUNT(*) AS total_customers
FROM workspace.default.silver_customers
GROUP BY marital;

---------------------------------------------------------------
-- 6. Total Revenue
---------------------------------------------------------------

SELECT
    ROUND(SUM(amount),2) AS total_revenue
FROM workspace.default.transactions;

---------------------------------------------------------------
-- 7. Average Transaction Amount
---------------------------------------------------------------

SELECT
    ROUND(AVG(amount),2) AS average_transaction
FROM workspace.default.transactions;

---------------------------------------------------------------
-- 8. Product-wise Revenue
---------------------------------------------------------------

SELECT
    product,
    ROUND(SUM(amount),2) AS revenue
FROM workspace.default.transactions
GROUP BY product
ORDER BY revenue DESC;

---------------------------------------------------------------
-- 9. Product-wise Transaction Count
---------------------------------------------------------------

SELECT
    product,
    COUNT(*) AS total_transactions
FROM workspace.default.transactions
GROUP BY product
ORDER BY total_transactions DESC;

---------------------------------------------------------------
-- 10. Transaction Status Summary
---------------------------------------------------------------

SELECT
    status,
    COUNT(*) AS total_transactions
FROM workspace.default.transactions
GROUP BY status;

---------------------------------------------------------------
-- 11. Offer Performance
---------------------------------------------------------------

SELECT
    offer_type,
    COUNT(*) AS offers_sent,
    SUM(CASE WHEN accepted='Yes' THEN 1 ELSE 0 END) AS accepted
FROM workspace.default.offers
GROUP BY offer_type;

---------------------------------------------------------------
-- 12. Channel Performance
---------------------------------------------------------------

SELECT
    channel,
    COUNT(*) AS offers_sent,
    SUM(CASE WHEN accepted='Yes' THEN 1 ELSE 0 END) AS accepted
FROM workspace.default.offers
GROUP BY channel;

---------------------------------------------------------------
-- 13. Offer Acceptance Rate
---------------------------------------------------------------

SELECT
    offer_type,

    ROUND(
        SUM(CASE WHEN accepted='Yes' THEN 1 ELSE 0 END)
        *100.0/
        COUNT(*),
        2
    ) AS acceptance_rate

FROM workspace.default.offers

GROUP BY offer_type

ORDER BY acceptance_rate DESC;

---------------------------------------------------------------
-- 14. Monthly Revenue
---------------------------------------------------------------

SELECT

date_format(transaction_date,'MMM') AS month,

ROUND(SUM(amount),2) AS revenue

FROM workspace.default.transactions

GROUP BY date_format(transaction_date,'MMM')

ORDER BY revenue DESC;

---------------------------------------------------------------
-- 15. Top 10 Highest Transactions
---------------------------------------------------------------

SELECT *

FROM workspace.default.transactions

ORDER BY amount DESC

LIMIT 10;

---------------------------------------------------------------
-- 16. Customer + Offer Join
---------------------------------------------------------------

SELECT

c.customer_id,

c.age,

c.job,

o.offer_type,

o.channel,

o.accepted

FROM workspace.default.silver_customers c

JOIN workspace.default.offers o

ON c.customer_id=o.customer_id;

---------------------------------------------------------------
-- 17. Customer + Transaction Join
---------------------------------------------------------------

SELECT

c.customer_id,

c.job,

t.product,

t.amount,

t.status

FROM workspace.default.silver_customers c

JOIN workspace.default.transactions t

ON c.customer_id=t.customer_id;

---------------------------------------------------------------
-- 18. Customers by Housing Loan
---------------------------------------------------------------

SELECT

housing,

COUNT(*) AS customers

FROM workspace.default.silver_customers

GROUP BY housing;

---------------------------------------------------------------
-- 19. Customers by Personal Loan
---------------------------------------------------------------

SELECT

loan,

COUNT(*) AS customers

FROM workspace.default.silver_customers

GROUP BY loan;

---------------------------------------------------------------
-- 20. Campaign Response
---------------------------------------------------------------

SELECT

y,

COUNT(*) AS customers

FROM workspace.default.silver_customers

GROUP BY y;

---------------------------------------------------------------
-- END OF SQL ANALYTICS
---------------------------------------------------------------