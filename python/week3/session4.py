import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ligar ao SQLite
conn = sqlite3.connect(Path("data") / "olist.db")
cursor = conn.cursor()

# query parametrizada
cursor.execute("SELECT * FROM olist_orders_dataset WHERE order_status = ?", ("delivered",))
rows = cursor.fetchmany(5)
for row in rows:
    logger.info(row)

# batch insert numa tabela de teste
cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_orders (
        order_id TEXT,
        status TEXT
    )
""")

orders = [
    ("order_001", "delivered"),
    ("order_002", "shipped"),
    ("order_003", "canceled"),
]

cursor.executemany("INSERT INTO test_orders VALUES (?, ?)", orders)
conn.commit()
logger.info("Batch insert concluído")

conn.close()