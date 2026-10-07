select
    date(pickup_ts)             as day,
    count(*)                    as trips,
    round(sum(total_amount), 2) as revenue
from {{ ref('stg_trips') }}
group by day
