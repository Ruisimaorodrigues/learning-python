{{ config(materialized='table') }}

with orders_enriched as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    order_id,
    customer_id,
    order_status,
    ordered_at,
    delivered_at,
    estimated_delivery_at,
    customer_city,
    customer_state,
    total_items_value,
    total_freight_value,
    total_items,
    total_payment_value,
    datediff('day', ordered_at, delivered_at) as days_to_deliver
from orders_enriched
where order_status = 'delivered'