-- Query 2: Top 10 customers por revenue total (GROUP BY + ORDER BY)
-- Objective: order customers and get only the top 10
-- Function used: row_number()
-- Expected result: 1 row per customer with his total revenue

SELECT 
	customer_id,
	SUM(sum_price) AS total_spent
FROM (
	SELECT 
		cus.customer_id,
		SUM(orit.price) AS sum_price,
		row_number() OVER(ORDER BY SUM(orit.price) DESC) AS rownumber
	FROM olist_customers_dataset cus
	JOIN olist_orders_dataset ord ON cus.customer_id = ord.customer_id
	JOIN olist_order_items_dataset orit ON ord.order_id = orit.order_id
	GROUP BY cus.customer_id
	) AS rankcustomers
WHERE rownumber <= 10
GROUP BY customer_id
ORDER BY total_spent DESC