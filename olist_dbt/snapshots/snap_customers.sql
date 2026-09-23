{% snapshot snap_customers %}

{{
    config(
        target_schema='main',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_city', 'customer_state']
    )
}}

select
    customer_id,
    customer_unique_id,
    customer_zip_code,
    customer_city,
    customer_state
from {{ ref('stg_customers') }}

{% endsnapshot %}