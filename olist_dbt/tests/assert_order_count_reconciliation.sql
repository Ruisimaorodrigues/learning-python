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
from staging_count s
cross join mart_count m
where s.total != m.total