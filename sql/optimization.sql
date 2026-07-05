-- ============================================================
-- Delta Lake & SQL Optimization
-- ============================================================

USE CATALOG workspace;
USE SCHEMA default;

-- ============================================================
-- 1. Show Table Details
-- ============================================================

DESCRIBE DETAIL silver_customers;

DESCRIBE DETAIL transactions;

DESCRIBE DETAIL offers;

-- ============================================================
-- 2. Compute Table Statistics
-- ============================================================

ANALYZE TABLE silver_customers COMPUTE STATISTICS;

ANALYZE TABLE transactions COMPUTE STATISTICS;

ANALYZE TABLE offers COMPUTE STATISTICS;

-- ============================================================
-- 3. Compute Column Statistics
-- ============================================================

ANALYZE TABLE silver_customers
COMPUTE STATISTICS FOR COLUMNS
age,
job,
education;

-- ============================================================
-- 4. Explain Query Plan
-- ============================================================

EXPLAIN FORMATTED

SELECT
    customer_id,
    SUM(amount) AS revenue
FROM transactions
GROUP BY customer_id;

-- ============================================================
-- 5. Explain Join Plan
-- ============================================================

EXPLAIN FORMATTED

SELECT
    c.customer_id,
    c.job,
    t.amount
FROM silver_customers c
JOIN transactions t
ON c.customer_id = t.customer_id;

-- ============================================================
-- 6. Delta Optimization (Production)
-- ============================================================
-- These commands are for production Databricks workspaces.
-- They may not be supported in the Free Edition.

-- OPTIMIZE silver_customers;

-- OPTIMIZE transactions;

-- OPTIMIZE offers;

-- ============================================================
-- 7. Z-ORDER Optimization (Production)
-- ============================================================

-- OPTIMIZE transactions
-- ZORDER BY (customer_id);

-- OPTIMIZE offers
-- ZORDER BY (customer_id);

-- ============================================================
-- 8. Vacuum Old Files (Production)
-- ============================================================

-- VACUUM silver_customers RETAIN 168 HOURS;

-- ============================================================
-- 9. Example Broadcast Join
-- ============================================================

SELECT /*+ BROADCAST(c) */

t.customer_id,

c.job,

t.amount

FROM transactions t

JOIN silver_customers c

ON t.customer_id = c.customer_id;

-- ============================================================
-- 10. Partition Recommendation
-- ============================================================

/*

Recommended Partitions

transactions

Partition By:
transaction_date

offers

Partition By:
offer_date

Reason

Improves query performance

Reduces scan time

Improves cost efficiency

*/

-- ============================================================
-- END
-- ============================================================