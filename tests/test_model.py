import pandas as pd
import pytest

from src.urban_mobility.model import build_od_matrix, haversine_km


@pytest.fixture
def zones():
    return pd.DataFrame([
        {"zone": "A", "population": 1000, "jobs": 100, "services": 50, "leisure": 20, "latitude": -23.55, "longitude": -46.63},
        {"zone": "B", "population": 500, "jobs": 300, "services": 100, "leisure": 80, "latitude": -23.56, "longitude": -46.65},
        {"zone": "C", "population": 800, "jobs": 150, "services": 200, "leisure": 300, "latitude": -23.58, "longitude": -46.62},
    ])


def test_haversine_zero_distance():
    assert haversine_km(-23.5, -46.6, -23.5, -46.6) == 0


def test_matrix_has_interzonal_pairs_and_percentages_sum_per_origin(zones):
    result = build_od_matrix(zones, attraction_column="jobs", include_intrazonal=False)
    assert len(result) == 6
    assert (result.origin != result.destination).all()
    totals = result.groupby("origin").share_of_origin_pct.sum()
    assert all(abs(value - 100) < 1e-8 for value in totals)


def test_trips_sum_to_population_times_rate(zones):
    rate = 0.4
    result = build_od_matrix(zones, trip_rate=rate)
    assert result.estimated_trips.sum() == pytest.approx(zones.population.sum() * rate)


def test_missing_fields_fail(zones):
    with pytest.raises(ValueError, match="Missing required"):
        build_od_matrix(zones.drop(columns=["jobs"]))


def test_duplicate_zones_fail(zones):
    duplicated = pd.concat([zones, zones.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="unique"):
        build_od_matrix(duplicated)


def test_negative_attraction_fails(zones):
    zones.loc[0, "services"] = -1
    with pytest.raises(ValueError, match="non-negative"):
        build_od_matrix(zones, attraction_column="services")
