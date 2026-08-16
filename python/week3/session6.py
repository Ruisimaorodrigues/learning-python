from pathlib import Path
import csv
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

input_file = Path("data") / "olist_orders_dataset.csv"
db_path = Path("data") / "olist.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders_loaded (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp TEXT
    )
""")

with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [
        (row['order_id'], row['customer_id'], row['order_status'], row['order_purchase_timestamp'])
        for row in reader
    ]

cursor.executemany("""
    INSERT OR IGNORE INTO orders_loaded 
    (order_id, customer_id, order_status, order_purchase_timestamp)
    VALUES (?, ?, ?, ?)
""", rows)

conn.commit()
logger.info(f"Linhas inseridas: {cursor.rowcount}")

# verificar idempotência
cursor.execute("SELECT COUNT(*) FROM orders_loaded")
count = cursor.fetchone()[0]
logger.info(f"Total de ordens na tabela: {count}")

conn.close()