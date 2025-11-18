## Запуск

```
cd docker
docker compose up -d
```

MinIO (локальный S3)
http://localhost:9001
minioadmin + minioadmin123

Grafana
http://localhost:3000
admin + admin

🧱 Шаг 4 — Исправляем DAG (ОЧЕНЬ ВАЖНО)

Пароль должен быть minioadmin123, как в docker-compose.

Исправь так:

s3 = boto3.client(
"s3",
endpoint_url=MINIO_ENDPOINT,
aws_access_key_id="minioadmin",
aws_secret_access_key="minioadmin123",
)

🔄 Проверь 10 раз: пароль именно minioadmin123.

⸻

🚀 Шаг 5 — Поднимаем весь стек снова

docker compose up -d

⸻

⏳ Шаг 6 — Ждём, пока сработает airflow-init

Проверить:

docker logs geo-airflow-init

Должно быть:

User created successfully

⸻

🏗️ Шаг 7 — Создаём bucket в Minio

Открываешь:

http://localhost:9001

логин:

minioadmin / minioadmin123

→ Create Bucket
название:

geo-traffic

⸻

🏁 Шаг 9 — Запускаем DAG

В Airflow UI → DAGs → traffic_pipeline → Trigger DAG.

⸻

🔍 Шаг 10 — Проверяем Minio

В bucket должно появиться:

raw/traffic_2025....json

⸻

📊 Шаг 11 — Проверяем ClickHouse

curl "http://localhost:8123/?query=SELECT count(*) FROM geo_traffic.traffic_grid"

## Структура

```
geo-traffic/
│
├── docker/
│ ├── docker-compose.yml # главный docker-compose
│ ├── airflow/
│ │ ├── Dockerfile
│ │ └── requirements.txt
│ ├── spark/
│ │ ├── Dockerfile
│ │ └── spark-defaults.conf
│ ├── minio/
│ │ ├── config.env
│ ├── clickhouse/
│ │ ├── Dockerfile (опционально)
│ │ ├── init.sql
│ └── grafana/
│ ├── provisioning/
│ │ └── dashboards/
│ │ └── traffic_dashboard.json
│ └── datasources/
│ └── clickhouse.yml
│
├── airflow/
│ ├── dags/
│ │ ├── generate_raw_traffic.py # DAG генерации сырых данных
│ │ ├── spark_etl.py # DAG для Spark ETL
│ │ └── load_to_clickhouse.py # DAG загрузки в CH
│ └── scripts/
│ └── helpers.py
│
├── generator/
│ ├── osm_graph_builder.py # скачивание/кеширование дорог Москвы
│ ├── route_generator.py # построение маршрутов по OSM
│ ├── simulate_cars.py # движение машин по маршрутам
│ └── write_to_s3.py # запись JSON в MinIO (S3)
│
├── spark/
│ ├── jobs/
│ │ ├── traffic_etl.py # агрегация скорости/плотности
│ │ └── utils.py
│ └── submit.sh # запуск spark-submit в контейнере
│
├── clickhouse/
│ ├── create_tables.sql # создаём traffic_grid
│ ├── insert_test.sql
│ └── queries/
│ └── traffic_heatmap.sql
│
├── grafana/
│ ├── dashboards/
│ │ └── traffic_dashboard.json
│ └── notes.md
│
├── config/
│ ├── settings.env # переменные окружения проекта
│ └── paths.yml # пути к S3 и т.д.
│
└── README.md # документация проекта
```