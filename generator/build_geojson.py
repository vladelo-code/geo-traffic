import json


def build_geojson():
    import requests

    url = "http://localhost:8123/?query="

    sql = """
    SELECT
        rg.edge_id,
        rg.polyline,
        g.avg_speed
    FROM geo_traffic.road_geometry AS rg
    LEFT JOIN (
        SELECT
            edge_id,
            avg(avg_speed) AS avg_speed
        FROM geo_traffic.traffic_grid
        WHERE ts >= now() - INTERVAL 5 MINUTE
        GROUP BY edge_id
    ) AS g ON g.edge_id = rg.edge_id
    """

    resp = requests.get(url + sql)
    lines = resp.text.strip().split("\n")

    features = []
    for line in lines:
        edge_id, polyline_raw, avg_speed = line.split("\t")

        poly = json.loads(polyline_raw)

        coords = [[p[1], p[0]] for p in poly]  # lon, lat

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "edge_id": edge_id,
                "avg_speed": float(avg_speed) if avg_speed else None
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }


if __name__ == "__main__":
    out = build_geojson()
    with open("roads_traffic.geojson", "w") as f:
        json.dump(out, f)
