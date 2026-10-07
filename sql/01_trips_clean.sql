CREATE OR REPLACE TABLE analytics.trips
PARTITION BY DATE(pickup_ts)
CLUSTER BY pu_location_id
AS
SELECT
  tpep_pickup_datetime  AS pickup_ts,
  tpep_dropoff_datetime AS dropoff_ts,
  PULocationID          AS pu_location_id,
  DOLocationID          AS do_location_id,
  passenger_count,
  trip_distance,
  fare_amount,
  tip_amount,
  total_amount
FROM raw.yellow_trips
WHERE tpep_pickup_datetime >= '2024-01-01'
  AND tpep_pickup_datetime <  '2024-02-01'
  AND tpep_dropoff_datetime >= tpep_pickup_datetime
  AND trip_distance > 0
  AND fare_amount > 0;