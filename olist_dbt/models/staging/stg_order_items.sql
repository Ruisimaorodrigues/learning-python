{{ config(materialized='view') }}

with source as (
    select *
    from read_csv_auto('{{ env_var("OLIST_DATA_PATH", "../data") }}/olist_order_items_dataset.csv')
),

renamed as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date::timestamp as shipping_limit_at,
        price,
        freight_value
    from source
)

select * from renamed