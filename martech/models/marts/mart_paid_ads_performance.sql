with google_ads as (
    select
        date,
        'google' as channel,
        campaign_id,
        campaign_name,
        impressions,
        clicks,
        spend,
        conversions
    from {{ ref('stg_raw_google_ads') }}
),

meta_ads as (
    select
        date,
        'meta' as channel,
        campaign_id,
        campaign_name,
        impressions,
        clicks,
        spend,
        conversions
    from {{ ref('stg_raw_meta_ads') }}
),

paid_ads as (
    select * from google_ads
    union all
    select * from meta_ads
)

select
    date,
    channel,
    campaign_id,
    campaign_name,
    impressions,
    clicks,
    spend,
    conversions,
    case when impressions > 0 then clicks * 1.0 / impressions end as ctr,
    case when clicks > 0 then spend / clicks end as cpc,
    case when impressions > 0 then spend * 1000.0 / impressions end as cpm,
    case when clicks > 0 then conversions * 1.0 / clicks end as conversion_rate
from paid_ads
