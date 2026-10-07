from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PY = "/home/airflow/tools/bin/python"
DBT = "/home/airflow/tools/bin/dbt"

with DAG(
    dag_id="taxi_monthly",
    start_date=datetime(2024, 1, 1),
    schedule=None,                  # manual trigger for now
    catchup=False,
    params={"ym": "2024-03"},       # month to load, e.g. 2024-03
    tags=["taxi"],
) as dag:

    load_taxi_month = BashOperator(
        task_id="load_taxi_month",
        bash_command=f"cd /opt/project && {PY} ingestion/load_taxi.py {{{{ params.ym }}}}",
        retries=2,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd /opt/project/dbt && {DBT} build --profiles-dir . "
            "--target-path /tmp/dbt_target --log-path /tmp/dbt_logs"
        ),
    )

    load_taxi_month >> dbt_build
