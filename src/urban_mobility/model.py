from __future__ import annotations

import math
from typing import Final

import pandas as pd

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "zone",
    "population",
    "jobs",
    "services",
    "leisure",
    "latitude",
    "longitude",
)
ATTRACTION_COLUMNS: Final[set[str]] = {"jobs", "services", "leisure"}
EARTH_RADIUS_KM: Final[float] = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return great-circle distance between two points in kilometers."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(min(1.0, a)))


def build_od_matrix(
    zones: pd.DataFrame,
    attraction_column: str = "jobs",
    alpha: float = 1.0,
    beta: float = 0.15,
    trip_rate: float = 0.6,
    include_intrazonal: bool = False,
) -> pd.DataFrame:
    """Build a synthetic gravity-model OD table from zone attributes.

    The output is modeled, not observed. Productions are population * trip_rate;
    destination choice is proportional to attraction**alpha * exp(-beta * distance).
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(zones.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if attraction_column not in ATTRACTION_COLUMNS:
        raise ValueError(f"attraction_column must be one of {sorted(ATTRACTION_COLUMNS)}")
    if alpha < 0 or beta < 0 or trip_rate <= 0:
        raise ValueError("alpha and beta must be non-negative; trip_rate must be positive")

    data = zones.loc[:, REQUIRED_COLUMNS].copy()
    if data.empty:
        raise ValueError("At least one zone is required")
    if data["zone"].isna().any() or data["zone"].astype(str).str.strip().eq("").any():
        raise ValueError("Zone names must be non-empty")
    data["zone"] = data["zone"].astype(str)
    if data["zone"].duplicated().any():
        raise ValueError("Zone names must be unique")

    numeric = ["population", "jobs", "services", "leisure", "latitude", "longitude"]
    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    if data[numeric].isna().any().any() or not data[numeric].map(math.isfinite).all().all():
        raise ValueError("Numeric fields must contain finite values")
    if (data[["population", "jobs", "services", "leisure"]] < 0).any().any():
        raise ValueError("Population and attraction values must be non-negative")
    if not data["latitude"].between(-90, 90).all() or not data["longitude"].between(-180, 180).all():
        raise ValueError("Coordinates must be valid latitude/longitude values")
    if not include_intrazonal and len(data) < 2:
        raise ValueError("At least two zones are required when intrazonal trips are excluded")
    if data[attraction_column].sum() <= 0:
        raise ValueError(f"At least one zone must have positive {attraction_column} attraction")

    rows: list[dict[str, float | str]] = []
    for origin in data.itertuples(index=False):
        candidates = data if include_intrazonal else data[data.zone != origin.zone]
        weights: list[tuple[object, float, float]] = []
        for destination in candidates.itertuples(index=False):
            distance = haversine_km(origin.latitude, origin.longitude, destination.latitude, destination.longitude)
            attraction = float(getattr(destination, attraction_column))
            weight = (attraction ** alpha) * math.exp(-beta * distance)
            weights.append((destination, distance, weight))
        weight_sum = sum(item[2] for item in weights)
        production = float(origin.population) * trip_rate
        if weight_sum <= 0:
            if production > 0:
                raise ValueError(f"No reachable destination attraction for origin {origin.zone}")
            continue
        for destination, distance, weight in weights:
            trips = production * weight / weight_sum
            rows.append({
                "origin": origin.zone,
                "destination": destination.zone,
                "distance_km": distance,
                "estimated_trips": trips,
                "share_of_origin_pct": 100 * weight / weight_sum,
            })

    result = pd.DataFrame(rows)
    if result.empty:
        return pd.DataFrame(columns=["origin", "destination", "distance_km", "estimated_trips", "share_of_origin_pct", "share_total_pct"])
    total = result["estimated_trips"].sum()
    result["share_total_pct"] = 100 * result["estimated_trips"] / total if total else 0.0
    return result.sort_values(["origin", "estimated_trips"], ascending=[True, False]).reset_index(drop=True)
