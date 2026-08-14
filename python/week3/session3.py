from pathlib import Path
import csv

file_path = Path("data") / "olist_orders_dataset.csv"

with open(file_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 5:
            break
        print(row)