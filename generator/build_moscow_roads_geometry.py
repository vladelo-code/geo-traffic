import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import requests

# Примерный bbox Москвы (можешь потом подправить)
# [south, west, north, east]
MOSCOW_BBOX = (55.3, 37.2, 56.1, 37.9)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

OUTPUT_PATH = Path(__file__).with_name("roads_moscow_geometry.json")


def build_overpass_query(bbox: Tuple[float, float, float, float]) -> str:
    south, west, north, east = bbox
    # Ищем все дороги highway=*
    query = f"""
    [out:json][timeout:900];
    (
      way["highway"]({south},{west},{north},{east});
    );
    (._;>;);
    out body;
    """
    return query


def fetch_osm_data() -> Dict:
    query = build_overpass_query(MOSCOW_BBOX)

    print("Запрашиваю данные дорог Москвы из Overpass API...")
    resp = requests.post(OVERPASS_URL, data={"data": query})
    resp.raise_for_status()

    data = resp.json()
    print(f"Получено элементов: {len(data.get('elements', []))}")
    return data


def build_road_geometries(osm_data: Dict) -> List[Dict]:
    elements = osm_data["elements"]

    # Сохраняем все ноды в словарь: id -> (lat, lon)
    nodes: Dict[int, Tuple[float, float]] = {}
    ways: List[Dict] = []

    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lat"], el["lon"])

    for el in elements:
        if el["type"] == "way":
            node_ids = el.get("nodes", [])
            coords = []
            for nid in node_ids:
                if nid in nodes:
                    lat, lon = nodes[nid]
                    coords.append([lat, lon])

            # Отбрасываем слишком короткие ways
            if len(coords) < 2:
                continue

            way_id = el["id"]
            ways.append(
                {
                    "edge_id": str(way_id),
                    "polyline": coords,
                }
            )

    print(f"Собрано дорожных сегментов (ways): {len(ways)}")
    return ways


def save_geometries(ways: List[Dict], output: Path) -> None:
    print(f"Сохраняю геометрию в {output} ...")
    with output.open("w", encoding="utf-8") as f:
        json.dump(ways, f)
    print("Готово.")


def main():
    start = time.time()
    osm_data = fetch_osm_data()
    ways = build_road_geometries(osm_data)
    save_geometries(ways, OUTPUT_PATH)
    print(f"Завершено за {time.time() - start:.1f} секунд")


if __name__ == "__main__":
    main()
