{% snapshot snap_dim_customers %}

{{
    config(
        target_schema='main',
        unique_key='customer_sk',
        strategy='check',
        check_cols=['customer_city', 'customer_state', 'customer_zip_code']
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,
    customer_id,
    customer_unique_id,
    customer_zip_code,
    customer_city,
    customer_state
from {{ ref('stg_customers') }}

{% endsnapshot %}