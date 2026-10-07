FROM apache/airflow:3.1.0
RUN python -m venv /home/airflow/tools \
 && /home/airflow/tools/bin/pip install --no-cache-dir dbt-bigquery google-cloud-bigquery google-cloud-storage requests pandas pyarrow
