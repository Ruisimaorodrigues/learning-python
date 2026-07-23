-- Query 4: Running Total de Revenue Acumulado ao longo do tempo
-- Objective: create a runnig total over time
-- Function used: SUM() OVER
-- Expected result: 1 row per order item done, summing its price over time
SELECT 
    t1.order_id,
    t1.order_item_id,
    t1.seller_id,
    t1.price,
    ord.order_purchase_timestamp,
    SUM(t1.price) OVER (
        ORDER BY ord.order_purchase_timestamp
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM olist_order_items_dataset t1
JOIN olist_orders_dataset ord ON t1.order_id = ord.order_id
ORDER BY ord.order_purchase_timestamp;