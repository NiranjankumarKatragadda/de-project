select
    z.borough,
    z.zone,
    count(*)                    as trips,
    round(sum(t.total_amount), 2) as revenue
from {{ ref('stg_trips') }} t
join {{ ref('dim_zone') }} z
  on t.pu_location_id = z.zone_id
group by z.borough, z.zone
