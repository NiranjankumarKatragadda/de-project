import json
import random
import sys
import time
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1

PROJECT = "retail-dev-nk2026"
TOPIC = "taxi-events"


def make_event() -> dict:
    distance = round(random.uniform(0.5, 15), 2)
    fare = round(3 + distance * 2.5 + random.uniform(0, 5), 2)
    tip = round(fare * random.choice([0, 0, 0.1, 0.15, 0.2]), 2)
    return {
        "event_id": str(uuid.uuid4()),
        "event_ts": datetime.now(timezone.utc).isoformat(),
        "pu_location_id": random.randint(1, 263),
        "do_location_id": random.randint(1, 263),
        "passenger_count": random.randint(1, 4),
        "trip_distance": distance,
        "fare_amount": fare,
        "tip_amount": tip,
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, TOPIC)

    for i in range(1, n + 1):
        event = make_event()
        message_id = publisher.publish(
            topic_path, json.dumps(event).encode("utf-8"), source="simulator"
        ).result()
        print(f"{i}/{n} published {event['event_id'][:8]} fare={event['fare_amount']} (msg {message_id})")
        time.sleep(delay)
