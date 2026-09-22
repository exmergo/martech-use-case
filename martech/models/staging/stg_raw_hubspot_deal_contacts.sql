with source as (
    select * from {{ source('main', 'raw_hubspot_deal_contacts') }}
),

renamed as (
    select
        deal_id,
        contact_id
    from source
)

select * from renamed
