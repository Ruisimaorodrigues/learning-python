-- Este teste falha se o número de ordens delivered no mart
-- for diferente do número na staging

with staging_count as (
    select count(*) as total
    from {{ ref('stg_orders') }}
    where order_status = 'delivered'
),

mart_count as (
    select count(*) as total
    from {{ ref('mart_orders') }}
)

select 1
from staging_count s, mart_count m
where s.total != m.total