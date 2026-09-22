with source as (
    select * from {{ source('main', 'raw_hubspot_contacts') }}
),

renamed as (
    select
        contact_id,
        created_at,
        source,
        campaign_id,
        campaign_name,
        lifecycle_stage
    from source
)

select * from renamed
