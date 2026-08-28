{{ config(materialized='view') }}

with source as (
    select *
    from read_csv_auto('{{ env_var("OLIST_DATA_PATH", "../data") }}/olist_orders_dataset.csv')
),

renamed as (
    select
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp::timestamp  as ordered_at,
        order_delivered_customer_date::timestamp as delivered_at,
        order_estimated_delivery_date::timestamp as estimated_delivery_at
    from source
)

select * from renamed