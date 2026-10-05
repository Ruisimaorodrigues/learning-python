{{ config(materialized='view') }}

with source as (
    select *
    from read_csv_auto('C:/Users/ruisi/learning-python/data/olist_sellers_dataset.csv')
),

renamed as (
    select
        seller_id,
        seller_zip_code_prefix as seller_zip_code,
        seller_city,
        seller_state
    from source
)

select * from renamed