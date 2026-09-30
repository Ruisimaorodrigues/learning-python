import duckdb
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = duckdb.connect('C:/Users/ruisi/learning-python/olist_dbt/dev.duckdb')

# Query directa ao mart
total_revenue = conn.execute("""
    SELECT round(sum(total_payment_value), 2) as total_revenue
    FROM mart_orders
    WHERE order_status = 'delivered'
""").fetchone()[0]

total_orders = conn.execute("""
    SELECT count(*) as total_orders
    FROM mart_orders
    WHERE order_status = 'delivered'
""").fetchone()[0]

avg_days = conn.execute("""
    SELECT round(avg(days_to_deliver), 2) as avg_days
    FROM mart_orders
    WHERE order_status = 'delivered'
    AND days_to_deliver is not null
""").fetchone()[0]

logger.info(f"Total Revenue (BRL): {total_revenue}")
logger.info(f"Total Orders: {total_orders}")
logger.info(f"Avg Days to Deliver: {avg_days}")

# Reconciliação contra staging
total_revenue_raw = conn.execute("""
    SELECT round(sum(payment_value), 2)
    FROM stg_payments p
    JOIN stg_orders o ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
""").fetchone()[0]

logger.info(f"Total Revenue from raw staging: {total_revenue_raw}")
logger.info(f"Diferença: {round(total_revenue - total_revenue_raw, 2)}")

conn.close()