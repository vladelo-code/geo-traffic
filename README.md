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