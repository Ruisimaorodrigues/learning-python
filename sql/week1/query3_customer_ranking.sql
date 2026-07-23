-- Query 3: Customers Ranking in each state with RANK() OVER PARTITION BY
-- Objective: rank Customers by total spent, for each state
-- Function used: rank()
-- Expected result: 1 row per customer with total spending, and its rank

With total_spent AS (
	SELECT customer_id, sum(payment_value) as total_spent			
	FROM olist_orders_dataset ord
	JOIN olist_order_payments_dataset paym on ord.order_id = paym.order_id
	group by customer_id
)

SELECT 	cus.customer_state,
		tp.customer_id,
		tp.total_spent,
		RANK() OVER (PARTITION BY cus.customer_state ORDER BY TP.total_spent DESC) as ranking
FROM total_spent tp
JOIN olist_customers_dataset cus on tp.customer_id = cus.customer_id
