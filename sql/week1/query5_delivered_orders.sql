-- Query 5: CTE that filters only delivered orders, then aggregates revenue by State.
-- Objective: filter for delivered orders, then aggregate revenue by Brazilian State.
-- Function used: SUM(), GROUP BY, CTE
-- Expected result: 1 row per State with aggregated revenue.

WITH delivered AS (
    SELECT order_id, customer_id 
    FROM olist_orders_dataset 
    WHERE order_status = 'delivered'
)
SELECT 
    cust.customer_state,
    SUM(oit.price) AS total_revenue
FROM delivered del
JOIN olist_order_items_dataset oit ON del.order_id = oit.order_id
JOIN olist_customers_dataset cust ON del.customer_id = cust.customer_id
GROUP BY cust.customer_state
ORDER BY total_revenue DESC;
