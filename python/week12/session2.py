import duckdb

conn = duckdb.connect('C:/Users/ruisi/learning-python/olist_dbt/dev.duckdb')

customer_id = '06b8999e2fba1a1fbc88172c00ba8bc7'

rows = conn.execute(f"""
    SELECT customer_id, customer_city, customer_state, dbt_valid_from, dbt_valid_to
    FROM snap_customers
    WHERE customer_id = '{customer_id}'
    ORDER BY dbt_valid_from
""").fetchall()

for row in rows:
    print(row)

conn.close()