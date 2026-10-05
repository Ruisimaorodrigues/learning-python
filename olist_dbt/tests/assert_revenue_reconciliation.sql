-- Este teste falha se a diferença entre mart e staging for > 0
-- Reconcilia revenue total entre mart_orders e stg_payments

with mart_revenue as (
    select round(sum(total_payment_value), 2) as total
    from {{ ref('mart_orders') }}
),

staging_revenue as (
    select round(sum(p.payment_value), 2) as total
    from {{ ref('stg_payments') }} p
    join {{ ref('stg_orders') }} o on p.order_id = o.order_id
    where o.order_status = 'delivered'
)

select 1
from mart_revenue m, staging_revenue s
where abs(m.total - s.total) > 0.01