CREATE
DATABASE IF NOT EXISTS geo_traffic;

CREATE TABLE IF NOT EXISTS geo_traffic.traffic_grid
(
    ts
    DateTime,
    grid_lat
    Int32,
    grid_lon
    Int32,
    avg_speed
    Float64,
    cars_count
    Int32,
    lat
    Float64,
    lon
    Float64,
    edge_id
    String
)
    ENGINE = MergeTree
(
)
    ORDER BY
(
    ts,
    grid_lat,
    grid_lon
);