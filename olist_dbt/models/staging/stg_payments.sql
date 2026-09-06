{{ config(materialized='view') }}

with source as (
    select *
    from read_csv_auto('C:/Users/ruisi/learning-python/data/olist_order_payments_dataset.csv')
),

renamed as (
    select
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
    from source
)

select * from renamed