from ingestion.load_taxi import URL


def test_url_format():
    url = URL.format(ym="2024-01")
    assert url.endswith("yellow_tripdata_2024-01.parquet")
