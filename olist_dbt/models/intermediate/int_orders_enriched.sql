{{ config(materialized='view') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_items as (
    select
        order_id,
        sum(price) as total_items_value,
        sum(freight_value) as total_freight_value,
        count(*) as total_items
    from {{ ref('stg_order_items') }}
    group by order_id
),

payments as (
    select
        order_id,
        sum(payment_value) as total_payment_value
    from {{ ref('stg_payments') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.ordered_at,
    o.delivered_at,
    o.estimated_delivery_at,
    c.customer_city,
    c.customer_state,
    oi.total_items_value,
    oi.total_freight_value,
    oi.total_items,
    p.total_payment_value
from orders o
left join customers c on o.customer_id = c.customer_id
left join order_items oi on o.order_id = oi.order_id
left join payments p on o.order_id = p.order_id