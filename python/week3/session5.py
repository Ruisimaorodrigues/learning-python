from pathlib import Path
import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

input_file = Path("data") / "olist_orders_dataset.csv"
output_file = Path("data") / "delivered_orders_with_days.csv"

# diagnóstico
with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    statuses = {}
    for row in reader:
        s = row['order_status']
        statuses[s] = statuses.get(s, 0) + 1

for status, count in sorted(statuses.items()):
    logger.info(f"Status '{status}': {count} ordens")

results = []
with open(input_file, mode="r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["order_status"] != "delivered":  # corrigido
            continue

        if not row["order_delivered_customer_date"]:
            logger.warning(f"Data de entrega vazia na ordem {row['order_id']}.")
            continue

        try:
            purchase = datetime.strptime(row["order_purchase_timestamp"], "%Y-%m-%d %H:%M:%S")
            delivered = datetime.strptime(row["order_delivered_customer_date"], "%Y-%m-%d %H:%M:%S")
            days = (delivered - purchase).days
            results.append({
                "order_id": row["order_id"],
                "days_to_deliver": days
            })
        except (ValueError, KeyError) as e:
            logger.warning(f"Erro na ordem {row.get('order_id', 'desconhecido')}: {e}")

logger.info(f"Total de pedidos processados: {len(results)}")

with open(output_file, mode="w", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "days_to_deliver"])
    writer.writeheader()
    writer.writerows(results)

logger.info(f"Ficheiro escrito em {output_file}")