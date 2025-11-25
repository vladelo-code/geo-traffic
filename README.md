## Запуск

```
cd docker
docker compose up -d
```

MinIO (локальный S3)
http://localhost:9001/
minioadmin + minioadmin123

надо создать bucket "geo-traffic"

Запускаем DAG

http://localhost:8080/home
airflow + airflow
В Airflow UI → DAGs → traffic_pipeline → Trigger DAG.

Проверяем ClickHouse
**http://localhost:8123/**

Сама интерактивная карта
http://localhost:8090/

## Структура

```
(.venv) ~/Documents/PyCharm/geo-traffic git:[main]
tree
.
├── README.md
├── airflow
│   ├── dags
│   │   ├── __pycache__
│   │   │   ├── traffic_dag.cpython-38.pyc
│   │   │   └── traffic_generator.cpython-38.pyc
│   │   ├── roads_moscow.json
│   │   ├── traffic.json
│   │   ├── traffic_dag.py
│   │   └── traffic_generator.py
│   ├── logs
│   │   ├── dag_id=traffic_pipeline
│   │   │   ├── run_id=manual__2025-11-25T11:10:59.528857+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       ├── attempt=1.log
│   │   │   │       └── attempt=2.log
│   │   │   ├── run_id=manual__2025-11-25T11:14:32.211044+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=manual__2025-11-25T11:14:53.479704+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=manual__2025-11-25T11:18:50.319924+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=manual__2025-11-25T11:44:57.898579+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   ├── attempt=1.log
│   │   │   │   │   └── attempt=2.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:05:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       ├── attempt=1.log
│   │   │   │       └── attempt=2.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:10:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:15:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:20:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:25:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:30:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:35:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   ├── attempt=1.log
│   │   │   │   │   └── attempt=2.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   ├── run_id=scheduled__2025-11-25T11:40:00+00:00
│   │   │   │   ├── task_id=generate
│   │   │   │   │   └── attempt=1.log
│   │   │   │   ├── task_id=load_clickhouse
│   │   │   │   │   └── attempt=1.log
│   │   │   │   └── task_id=upload_minio
│   │   │   │       └── attempt=1.log
│   │   │   └── run_id=scheduled__2025-11-25T11:45:00+00:00
│   │   │       ├── task_id=generate
│   │   │       │   └── attempt=1.log
│   │   │       ├── task_id=load_clickhouse
│   │   │       │   └── attempt=1.log
│   │   │       └── task_id=upload_minio
│   │   │           └── attempt=1.log
│   │   ├── dag_processor_manager
│   │   │   └── dag_processor_manager.log
│   │   └── scheduler
│   │       ├── 2025-11-25
│   │       │   └── traffic_dag.py.log
│   │       ├── 2025-11-25 2
│   │       └── latest -> 2025-11-25
│   └── plugins
├── api
│   ├── __pycache__
│   │   └── main.cpython-310.pyc
│   └── main.py
├── clickhouse
│   ├── config
│   │   └── users.xml
│   └── init.sql
├── docker
│   └── docker-compose.yml
├── frontend-map
│   └── index.html
├── generator
│   ├── build_geojson.py
│   ├── build_moscow_roads.py
│   ├── build_moscow_roads_geometry.py
│   ├── load_road_geometry_to_clickhouse.py
│   └── roads_moscow_geometry.json
└── tileserver
    ├── config.json
    └── styles
        └── roads_style.json

76 directories, 65 files
```