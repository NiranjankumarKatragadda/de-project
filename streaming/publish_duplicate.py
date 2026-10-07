import json
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic = publisher.topic_path("retail-dev-nk2026", "taxi-events")

event = {
    "event_id": str(uuid.uuid4()),
    "event_ts": datetime.now(timezone.utc).isoformat(),
    "pu_location_id": 132,
    "do_location_id": 161,
    "passenger_count": 1,
    "trip_distance": 5.5,
    "fare_amount": 21.0,
    "tip_amount": 3.0,
}
for _ in range(2):  # the same event_id, sent twice
    publisher.publish(topic, json.dumps(event).encode("utf-8")).result()
print("published duplicate event", event["event_id"])
