with source as (
    select
        "Date",
        "Close",
        "symbol"
    from 
        {{ source('dbsalesworkshop', 'commodities') }}
),

renamed as (
    select
        cast("Date" as date) as closing_date,
        "Close" as closing_value,
        symbol
    from
        source
)

select * from renamed
