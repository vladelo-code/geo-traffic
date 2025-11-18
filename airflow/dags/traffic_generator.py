import random
import json
from datetime import datetime
from pathlib import Path


def generate_traffic_grid():
    """
    Простая генерация "пробок" в сетке 10×10.
    Каждый grid — ячейка территории.
    """
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    rows = []
    for lat in range(10):
        for lon in range(10):
            avg_speed = random.uniform(5, 80)  # средняя скорость (км/ч)
            cars_count = random.randint(0, 50)  # машин в ячейке
            rows.append(
                {
                    "ts": now,
                    "grid_lat": lat,
                    "grid_lon": lon,
                    "avg_speed": avg_speed,
                    "cars_count": cars_count,
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
