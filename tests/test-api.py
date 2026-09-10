from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_trips_per_route():
    response = client.get("/analytics/trips-per-route")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "route_id" in data[0]
        assert "route_short_name" in data[0]
        assert "route_long_name" in data[0]
        assert "trip_count" in data[0]


def test_busiest_stops():
    response = client.get("/analytics/busiest-stops")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "stop_id" in data[0]
        assert "stop_name" in data[0]


def test_trips_by_hour():
    response = client.get("/analytics/trips-by-hour")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for item in data:
        assert "hour" in item
        assert "trip_count" in item
        assert isinstance(item["hour"], int)
        assert isinstance(item["trip_count"], int)
        assert 0 <= item["hour"] <= 23
        assert item["trip_count"] >= 0


def test_route_statistics():
    response = client.get("/analytics/routes/77119")

    assert response.status_code == 200

    data = response.json()

    assert data["route_id"] == "77119"
    assert data["total_trips"] == 153
    assert data["stops_served"] == 48
    assert data["average_stops_per_trip"] == 22.5


def test_route_statistics_values():
    response = client.get("/analytics/routes/77119")

    assert response.status_code == 200

    data = response.json()

    assert data["total_trips"] >= 0
    assert data["stops_served"] >= 0
    assert data["average_stops_per_trip"] >= 0


def test_route_not_found():
    response = client.get("/analytics/routes/132498")

    assert response.status_code == 404
    assert response.json()["detail"] == "Route 132498 not found"


# Regular endpoints

def test_database_health():
    response = client.get("/health/db")

    assert response.status_code == 200

    data = response.json()
    assert data["database"] == "connected"


def test_agencies():
    response = client.get("/agencies")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "agency_id" in data[0]
        assert "agency_name" in data[0]


def test_routes():
    response = client.get("/routes")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "route_id" in data[0]
        assert "route_short_name" in data[0]
        assert "route_long_name" in data[0]


def test_stops():
    response = client.get("/stops")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "stop_id" in data[0]
        assert "stop_name" in data[0]


def test_trips():
    response = client.get("/trips")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "trip_id" in data[0]
        assert "route_id" in data[0]


def test_stop_times():
    response = client.get("/stop-times")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "trip_id" in data[0]
        assert "stop_id" in data[0]
        assert "stop_sequence" in data[0]
