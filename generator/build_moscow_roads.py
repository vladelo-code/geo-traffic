import json
from pathlib import Path

import osmnx as ox


def build_moscow_roads(output_path: str):
    """
    Скачиваем дорожный граф Москвы и сохраняем упрощённый список "сегментов дорог"
    в JSON, чтобы потом использовать в генераторе трафика.

    На выход кладём список объектов вида:
    {
        "edge_id": int,
        "lat": float,
        "lon": float
    }

    lat/lon — это центр (центроид) сегмента дороги.
    """
    print("Загружаем дорожный граф Москвы из OSM...")
    # network_type="drive" — только дороги для машин
    G = ox.graph_from_place("Moscow, Russia", network_type="drive")

    print("Преобразуем граф в GeoDataFrame рёбер...")
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

    records = []
    print(f"Всего рёбер (сегментов дорог): {len(edges)}")

    for idx, row in edges.iterrows():
        geom = row.geometry
        centroid = geom.centroid  # shapely Point

        lat = float(centroid.y)
        lon = float(centroid.x)

        osmid = row.get("osmid", None)
        # osmid может быть числом или списком — нормализуем
        if isinstance(osmid, (list, tuple, set)):
            osmid = list(osmid)[0]

        records.append(
            {
                "edge_id": int(osmid) if osmid is not None else int(idx[1]) if isinstance(idx, tuple) else int(
                    idx
                ),
                "lat": lat,
                "lon": lon,
            }
        )

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Сохраняем {len(records)} сегментов в {out_path} ...")
    with out_path.open("w") as f:
        json.dump(records, f)

    print("Готово!")


if __name__ == "__main__":
    # Пишем сразу туда, откуда Airflow сможет прочитать
    default_output = Path(__file__).resolve().parents[1] / "airflow" / "dags" / "roads_moscow.json"
    build_moscow_roads(str(default_output))
