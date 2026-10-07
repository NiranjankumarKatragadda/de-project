from streaming.publish_events import make_event


def test_event_has_expected_fields():
    event = make_event()
    expected = {
        "event_id", "event_ts", "pu_location_id", "do_location_id",
        "passenger_count", "trip_distance", "fare_amount", "tip_amount",
    }
    assert set(event) == expected


def test_event_values_are_sensible():
    for _ in range(100):
        event = make_event()
        assert event["fare_amount"] > 0
        assert event["tip_amount"] >= 0
        assert 1 <= event["pu_location_id"] <= 263


def test_event_ids_are_unique():
    ids = {make_event()["event_id"] for _ in range(200)}
    assert len(ids) == 200
