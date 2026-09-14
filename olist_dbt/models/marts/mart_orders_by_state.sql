{{ config(materialized='table') }}

{% set states = ['SP', 'RJ', 'MG', 'RS', 'PR'] %}

with base as (
    select * from {{ ref('mart_orders') }}
),

top_states as (
    select
        customer_state,
        count(*) as total_orders,
        round(sum(total_payment_value), 2) as total_revenue,
        round(avg(days_to_deliver), 1) as avg_days_to_deliver
    from base
    {% if states %}
    where customer_state in (
        {% for state in states %}
            '{{ state }}'{% if not loop.last %},{% endif %}
        {% endfor %}
    )
    {% endif %}
    group by customer_state
    order by total_revenue desc
)

select * from top_states