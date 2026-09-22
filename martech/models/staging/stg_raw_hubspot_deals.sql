with source as (
    select * from {{ source('main', 'raw_hubspot_deals') }}
),

renamed as (
    select
        deal_id,
        contact_id,
        campaign_id,
        deal_amount,
        deal_status,
        closed_at
    from source
)

select * from renamed
