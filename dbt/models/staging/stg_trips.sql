select
    tpep_pickup_datetime  as pickup_ts,
    tpep_dropoff_datetime as dropoff_ts,
    PULocationID          as pu_location_id,
    DOLocationID          as do_location_id,
    passenger_count,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount,
    source_month
from {{ source('raw', 'yellow_trips') }}
where tpep_pickup_datetime >= '2024-01-01'
  and tpep_pickup_datetime <  '2024-04-01'
  and tpep_dropoff_datetime >= tpep_pickup_datetime
  and trip_distance > 0
  and fare_amount > 0
