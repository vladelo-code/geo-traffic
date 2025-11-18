from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import boto3
import requests

from traffic_generator import main as generate_traffic_file  # импортируем наш генератор

MINIO_ENDPOINT = "http://geo-minio:9000"
BUCKET_NAME = "geo-traffic"
CLICKHOUSE_URL = "http://geo-clickhouse:8123"


def generate_data():
    """
    Генерируем traffic.json в папке DAG'ов.
    """
    output_path = "/opt/airflow/dags/traffic.json"
    generate_traffic_file(output_path)


def upload_to_minio():
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin123",
    )

    file_path = "/opt/airflow/dags/traffic.json"
    object_key = f"raw/traffic_{datetime.utcnow().isoformat()}.json"

    with open(file_path, "rb") as f:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=f.read(),
        )


def load_clickhouse():
    file_path = "/opt/airflow/dags/traffic.json"
    with open(file_path) as f:
        data = json.load(f)

    rows = []
    for row in data:
        values = (
            f"'{row['ts']}'",
            row["grid_lat"],
            row["grid_lon"],
            row["avg_speed"],
            row["cars_count"],
        )
        rows.append("(" + ",".join(map(str, values)) + ")")

    sql = f"""
        INSERT INTO geo_traffic.traffic_grid
        (ts, grid_lat, grid_lon, avg_speed, cars_count)
        VALUES {",".join(rows)}
    """

    resp = requests.post(CLICKHOUSE_URL, params={"query": sql})
    resp.raise_for_status()


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}

with DAG(
        "traffic_pipeline",
        default_args=default_args,
        schedule_interval="*/5 * * * *",  # каждые 5 минут
        start_date=datetime(2024, 1, 1),
        catchup=False,
        tags=["geo", "traffic"],
) as dag:
    t1 = PythonOperator(
        task_id="generate",
        python_callable=generate_data,
    )

    t2 = PythonOperator(
        task_id="upload_minio",
        python_callable=upload_to_minio,
    )

    t3 = PythonOperator(
        task_id="load_clickhouse",
        python_callable=load_clickhouse,
    )

    t1 >> t2 >> t3
