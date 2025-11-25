import json
from pathlib import Path
from typing import Dict, Any, Iterable

import requests

CLICKHOUSE_URL = "http://localhost:8123"
TABLE = "geo_traffic.road_geometry"


def iter_json_each_row(data: Iterable[Dict[str, Any]]) -> Iterable[bytes]:
    """
    Генератор строк для ClickHouse формата JSONEachRow.
    Не держим всё в памяти, стримим построчно.
    """
    for item in data:
        # Убеждаемся, что edge_id — строка
        row = {
            "edge_id": str(item["edge_id"]),
            "polyline": item["polyline"],
        }
        line = json.dumps(row, ensure_ascii=False)
        yield (line + "\n").encode("utf-8")


def main() -> None:
    json_path = Path(__file__).with_name("roads_moscow_geometry.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Не найден файл {json_path}")

    print(f"Читаю {json_path} ...")
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Всего сегментов дорог: {len(data)}")

    query = f"INSERT INTO {TABLE} (edge_id, polyline) FORMAT JSONEachRow"

    print("Отправляю данные в ClickHouse...")
    resp = requests.post(
        CLICKHOUSE_URL,
        params={"query": query},
        data=iter_json_each_row(data),
    )
    resp.raise_for_status()
    print("Готово, вставка прошла успешно.")


if __name__ == "__main__":
    main()
