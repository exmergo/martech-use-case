with source as (
    select * from {{ source('main', 'raw_google_ads') }}
),

renamed as (
    select
        date,
        campaign_id,
        campaign_name,
        impressions,
        clicks,
        spend,
        conversions
    from source
)

select * from renamed
