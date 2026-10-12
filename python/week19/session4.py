import duckdb
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = duckdb.connect('C:/Users/ruisi/learning-python/olist_dbt/dev.duckdb')

logger.info("=== RECONCILIAÇÃO DE MÉTRICAS ===")

# 1. Total Revenue
revenue = conn.execute("""
    SELECT round(sum(total_payment_value), 2)
    FROM mart_orders
""").fetchone()[0]
logger.info(f"1. Total Revenue: {revenue} BRL")

# 2. Total Orders
orders = conn.execute("""
    SELECT count(*)
    FROM mart_orders
""").fetchone()[0]
logger.info(f"2. Total Orders: {orders}")

# 3. Average Days to Deliver
avg_days = conn.execute("""
    SELECT round(avg(days_to_deliver), 2)
    FROM mart_orders
    WHERE days_to_deliver is not null
""").fetchone()[0]
logger.info(f"3. Avg Days to Deliver: {avg_days}")

# 4. Revenue per State - top 5
logger.info("4. Revenue per State (top 5):")
rows = conn.execute("""
    SELECT customer_state, round(sum(total_payment_value), 2) as revenue
    FROM mart_orders
    GROUP BY customer_state
    ORDER BY revenue DESC
    LIMIT 5
""").fetchall()
for row in rows:
    logger.info(f"   {row[0]}: {row[1]} BRL")

# 5. Average Order Value
aov = conn.execute("""
    SELECT round(sum(total_payment_value) / count(distinct order_id), 2)
    FROM mart_orders
    WHERE total_payment_value > 0
""").fetchone()[0]
logger.info(f"5. Average Order Value: {aov} BRL")

# 6. Freight Rate
freight_rate = conn.execute("""
    SELECT round(sum(total_freight_value) / nullif(sum(total_items_value), 0) * 100, 2)
    FROM mart_orders
    WHERE total_items_value > 0
""").fetchone()[0]
logger.info(f"6. Freight Rate: {freight_rate}%")

logger.info("=== RECONCILIAÇÃO CONCLUÍDA ===")

conn.close()