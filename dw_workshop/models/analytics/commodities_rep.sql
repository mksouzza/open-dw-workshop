with commodities as (
    select
        closing_date,
        closing_value,
        symbol
    from
        {{ ref('stg_commodities') }}
)
select * from commodities
