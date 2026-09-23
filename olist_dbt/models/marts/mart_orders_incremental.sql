{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

with orders_enriched as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'customer_id']) }} as order_sk,
    order_id,
    customer_id,
    order_status,
    ordered_at,
    delivered_at,
    customer_state,
    total_items_value,
    total_payment_value,
    {{ days_between('ordered_at', 'delivered_at') }} as days_to_deliver,
    {{ brl_to_eur('total_payment_value') }} as total_payment_eur

from orders_enriched

{% if is_incremental() %}
    where ordered_at > (select max(ordered_at) from {{ this }})
{% endif %}