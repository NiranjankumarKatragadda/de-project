import sys
import logging
import requests
from pathlib import Path
from google.cloud import bigquery, storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("load_taxi")

PROJECT = "retail-dev-nk2026"
BUCKET = f"{PROJECT}-raw"
URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ym}.parquet"


def download(ym: str) -> Path:
    path = Path("data") / f"yellow_{ym}.parquet"
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        log.info("Already downloaded: %s", path)
        return path
    log.info("Downloading %s", ym)
    r = requests.get(URL.format(ym=ym), timeout=300)
    r.raise_for_status()
    path.write_bytes(r.content)
    return path


def upload(path: Path, ym: str) -> str:
    blob_name = f"taxi/yellow/{ym}/{path.name}"
    blob = storage.Client(project=PROJECT).bucket(BUCKET).blob(blob_name)
    if blob.exists():
        log.info("Already in GCS: %s", blob_name)
    else:
        log.info("Uploading %s", blob_name)
        blob.chunk_size = 8 * 1024 * 1024
        blob.upload_from_filename(path, timeout=600)
    return f"gs://{BUCKET}/{blob_name}"


def load_to_bq(uri: str, ym: str) -> None:
    client = bigquery.Client(project=PROJECT)
    staging = f"{PROJECT}.raw.yellow_trips_stg"
    target = f"{PROJECT}.raw.yellow_trips"

    # 1. Load the file into staging (replaces previous contents)
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_TRUNCATE",
    )
    job = client.load_table_from_uri(uri, staging, job_config=config)
    job.result()
    log.info("Staged %s rows", job.output_rows)

    # 2. Replace this month's rows in one transaction
    sql = f"""
    BEGIN TRANSACTION;
    DELETE FROM `{target}` WHERE source_month = @ym;
    INSERT INTO `{target}` SELECT *, @ym AS source_month FROM `{staging}`;
    COMMIT TRANSACTION;
    """
    params = [bigquery.ScalarQueryParameter("ym", "STRING", ym)]
    client.query(sql, job_config=bigquery.QueryJobConfig(query_parameters=params)).result()
    log.info("Month %s loaded into %s", ym, target)


if __name__ == "__main__":
    ym = sys.argv[1]  # e.g. 2024-01
    path = download(ym)
    uri = upload(path, ym)
    load_to_bq(uri, ym)