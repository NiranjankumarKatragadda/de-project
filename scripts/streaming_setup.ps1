# Streaming infrastructure for retail-dev-nk2026 (run once)
gcloud services enable pubsub.googleapis.com
gcloud pubsub topics create taxi-events
bq --location=US mk --dataset retail-dev-nk2026:streaming
bq mk --table --time_partitioning_field event_ts --schema "event_id:STRING,event_ts:TIMESTAMP,pu_location_id:INTEGER,do_location_id:INTEGER,passenger_count:INTEGER,trip_distance:FLOAT,fare_amount:FLOAT,tip_amount:FLOAT" retail-dev-nk2026:streaming.taxi_events
gcloud pubsub subscriptions create taxi-events-bq --topic=taxi-events --bigquery-table=retail-dev-nk2026:streaming.taxi_events --use-table-schema --drop-unknown-fields
