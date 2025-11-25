from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clickhouse_driver import Client
import json
import time
import os

ROADS_FILE = "/data/roads.json"

print("Loading road geometry...")
t0 = time.time()

if not os.path.exists(ROADS_FILE):
    print(f"ERROR: roads.json not found at {ROADS_FILE}")
    roads = []
else:
    with open(ROADS_FILE, "r") as f:
        roads = json.load(f)

if len(roads) == 0:
    print("WARNING: roads.json is EMPTY!")

GEOMETRY = {str(item["edge_id"]): item["polyline"] for item in roads}

print(f"Loaded {len(GEOMETRY)} roads in {time.time() - t0:.1f}s")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client(
    host="geo-clickhouse",
    port=9000,
    connect_timeout=3,
    send_receive_timeout=5
)


@app.get("/traffic")
def get_traffic():
    # получить последнюю метку времени
    latest_ts = client.execute("SELECT max(ts) FROM geo_traffic.traffic_grid")[0][0]

    rows = client.execute(
        """
        SELECT edge_id, avg_speed, cars_count
        FROM geo_traffic.traffic_grid
        WHERE ts = %(ts)s
        """,
        {"ts": latest_ts}
    )

    result = []
    for edge_id, avg_speed, cars_count in rows:
        eid = str(edge_id)
        polyline = GEOMETRY.get(eid)
        if polyline:
            result.append({
                "edge_id": eid,
                "avg_speed": avg_speed,
                "cars_count": cars_count,
                "polyline": polyline
            })

    return result
