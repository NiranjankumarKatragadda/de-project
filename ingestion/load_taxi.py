import sys
import requests
from pathlib import Path
from google.cloud import bigquery, storage

PROJECT = "retail-dev-nk2026"
BUCKET = f"{PROJECT}-raw"
URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ym}.parquet"

def download(ym: str) -> Path:
    path = Path("data") / f"yellow_{ym}.parquet"
    path.parent.mkdir(exist_ok=True)
    if not path.exists():
        r = requests.get(URL.format(ym=ym), timeout=120)
        r.raise_for_status()
        path.write_bytes(r.content)
    return path

def upload(path: Path, ym: str) -> str:
    blob_name = f"taxi/yellow/{ym}/{path.name}"
    blob = storage.Client(project=PROJECT).bucket(BUCKET).blob(blob_name)
    blob.chunk_size = 8 * 1024 * 1024  # 8 MB pieces
    blob.upload_from_filename(path, timeout=600)
    return f"gs://{BUCKET}/{blob_name}"

def load_to_bq(uri: str):
    client = bigquery.Client(project=PROJECT)
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_APPEND",
    )
    job = client.load_table_from_uri(uri, f"{PROJECT}.raw.yellow_trips", config)
    job.result()
    print(f"Loaded {job.output_rows} rows from {uri}")

if __name__ == "__main__":
    ym = sys.argv[1]  # e.g. 2024-01
    load_to_bq(upload(download(ym), ym))