import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# Настройки "сетки"
GRID_LAT_CELLS = 100
GRID_LON_CELLS = 100

# Путь к файлу с дорогами Москвы
ROADS_PATH = Path(__file__).with_name("roads_moscow.json")

# Глобальные переменные, чтобы не перерасчётовать каждый раз
_ROADS_CACHE: List[Dict] = []
_LAT_LON_BOUNDS: Tuple[float, float, float, float] = (0, 0, 0, 0)


def _load_roads() -> List[Dict]:
    global _ROADS_CACHE
    if _ROADS_CACHE:
        return _ROADS_CACHE

    if not ROADS_PATH.exists():
        raise FileNotFoundError(f"roads_moscow.json не найден по пути: {ROADS_PATH}")

    with ROADS_PATH.open() as f:
        _ROADS_CACHE = json.load(f)

    if not _ROADS_CACHE:
        raise ValueError("roads_moscow.json пустой — в нём нет сегментов дорог.")

    return _ROADS_CACHE


def _compute_bounds() -> Tuple[float, float, float, float]:
    """
    Считаем min/max lat/lon по всем сегментам.
    """
    global _LAT_LON_BOUNDS
    if any(_LAT_LON_BOUNDS):
        return _LAT_LON_BOUNDS

    roads = _load_roads()
    lats = [r["lat"] for r in roads]
    lons = [r["lon"] for r in roads]

    min_lat = min(lats)
    max_lat = max(lats)
    min_lon = min(lons)
    max_lon = max(lons)

    _LAT_LON_BOUNDS = (min_lat, max_lat, min_lon, max_lon)
    return _LAT_LON_BOUNDS


def latlon_to_grid(lat: float, lon: float) -> Tuple[int, int]:
    """
    Конвертация пары (lat, lon) в индексы grid_lat / grid_lon.
    """
    min_lat, max_lat, min_lon, max_lon = _compute_bounds()

    # Немного защищаемся от деления на ноль
    lat_range = max(max_lat - min_lat, 1e-9)
    lon_range = max(max_lon - min_lon, 1e-9)

    lat_norm = (lat - min_lat) / lat_range
    lon_norm = (lon - min_lon) / lon_range

    grid_lat = int(lat_norm * (GRID_LAT_CELLS - 1))
    grid_lon = int(lon_norm * (GRID_LON_CELLS - 1))

    # На всякий случай ограничим границы
    grid_lat = max(0, min(GRID_LAT_CELLS - 1, grid_lat))
    grid_lon = max(0, min(GRID_LON_CELLS - 1, grid_lon))

    return grid_lat, grid_lon


def generate_traffic_grid(sample_size: int = 500):
    """
    Генерируем "пробки" на реальных дорожных сегментах Москвы.
    Каждый сегмент берём из roads_moscow.json.
    """
    roads = _load_roads()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if sample_size > len(roads):
        sample_size = len(roads)

    sampled_roads = random.sample(roads, sample_size)

    rows = []
    for r in sampled_roads:
        lat = r["lat"]
        lon = r["lon"]

        grid_lat, grid_lon = latlon_to_grid(lat, lon)

        avg_speed = random.uniform(5, 80)  # км/ч
        cars_count = random.randint(0, 50)  # машин на сегменте

        rows.append(
            {
                "ts": now,
                "grid_lat": grid_lat,
                "grid_lon": grid_lon,
                "avg_speed": avg_speed,
                "cars_count": cars_count,
                "edge_id": r["edge_id"],
                "lat": lat,
                "lon": lon,
            }
        )

    return rows


def save_to_json(rows, path: str):
    path = Path(path)
    with path.open("w") as f:
        json.dump(rows, f)


def main(output_path: str = "traffic.json"):
    rows = generate_traffic_grid()
    save_to_json(rows, output_path)


if __name__ == "__main__":
    main()
