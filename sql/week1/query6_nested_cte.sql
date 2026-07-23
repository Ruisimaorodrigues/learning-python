-- Query 6 - Nested CTE with final filter per customer value.
-- Objective: filter for delivered orders → aggregated by customer → filter only for customers with expenses above 6k.
-- Function used: SUM(), ROW_number()
-- Expected result: 1 row per customer with revenue above 6000.

WITH delivered AS (
    SELECT order_id, customer_id
    FROM olist_orders_dataset
    WHERE order_status = 'delivered'
),
customer_revenue AS (
    SELECT 
        del.customer_id,
        SUM(oit.price) AS total_spent
    FROM delivered del
    JOIN olist_order_items_dataset oit ON del.order_id = oit.order_id
    GROUP BY del.customer_id
)
SELECT 
    customer_id,
    total_spent
FROM customer_revenue
WHERE total_spent > 6000
ORDER BY total_spent DESC