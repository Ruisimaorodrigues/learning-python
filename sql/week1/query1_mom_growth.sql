-- Query 1: MoM Revenue Growth
-- Objective: compare monthly revenue with previous month revenue
-- Function used: LAG() OVER (ORDER BY month)
-- Expected result: 1 row per month with revenue and monthly growth

SELECT 	STRFTIME('%Y-%m',shipping_limit_date) as month,
		SUM(price) as current_month_price,
		LAG(sum(price)) OVER (ORDER BY STRFTIME('%Y-%m',shipping_limit_date)) AS previous_month_price,
		ROUND((SUM(price) - LAG(sum(price)) OVER (ORDER BY STRFTIME('%Y-%m',shipping_limit_date))) 
		/ LAG(sum(price)) OVER (ORDER BY STRFTIME('%Y-%m',shipping_limit_date)),2)
		AS MOM_GROWTH
FROM olist_order_items_dataset
GROUP BY STRFTIME('%Y-%m',shipping_limit_date)
ORDER BY month