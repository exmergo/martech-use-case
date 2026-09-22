with ad_performance as (
    select
        campaign_id,
        channel,
        campaign_name,
        sum(spend) as spend
    from {{ ref('mart_paid_ads_performance') }}
    group by 1, 2, 3
),

attributed_deals as (
    select
        campaign_id,
        deal_id,
        deal_amount
    from {{ ref('int_deal_attribution') }}
    where deal_status = 'closed_won'
),

campaign_conversions as (
    select
        campaign_id,
        count(distinct deal_id) as conversions,
        sum(deal_amount) as revenue
    from attributed_deals
    group by 1
)

select
    a.campaign_id,
    a.channel,
    a.campaign_name,
    a.spend,
    coalesce(c.conversions, 0) as conversions,
    coalesce(c.revenue, 0) as revenue,
    case
        when coalesce(c.conversions, 0) > 0
            then a.spend / c.conversions
    end as cac,
    case
        when a.spend > 0
            then coalesce(c.revenue, 0) / a.spend
    end as roas
from ad_performance a
left join campaign_conversions c on a.campaign_id = c.campaign_id
