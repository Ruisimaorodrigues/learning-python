{{ config(materialized='view') }}

with source as (
    select *
    from read_csv_auto('{{ env_var("OLIST_DATA_PATH", "../data") }}/olist_customers_dataset.csv')
),

renamed as (
    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix as customer_zip_code,
        customer_city,
        customer_state
    from source
)

select * from renamed