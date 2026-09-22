with deal_contacts as (
    select
        deal_id,
        contact_id
    from {{ ref('stg_raw_hubspot_deal_contacts') }}
),

contacts as (
    select
        contact_id,
        campaign_id
    from {{ ref('stg_raw_hubspot_contacts') }}
),

deals as (
    select
        deal_id,
        deal_amount,
        deal_status
    from {{ ref('stg_raw_hubspot_deals') }}
)

select
    deal_contacts.deal_id,
    deal_contacts.contact_id,
    contacts.campaign_id,
    deals.deal_amount,
    deals.deal_status
from deal_contacts
inner join contacts
    on deal_contacts.contact_id = contacts.contact_id
inner join deals
    on deal_contacts.deal_id = deals.deal_id
