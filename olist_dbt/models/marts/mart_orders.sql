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
    {{ days_between('ordered_at', 'delivered_at') }} as days_to_deliver,
    {{ brl_to_eur('total_payment_value') }} as total_payment_eur,
    {{ safe_divide('total_items_value', 'total_items') }} as avg_item_price

from orders_enriched
where order_status = 'delivered'