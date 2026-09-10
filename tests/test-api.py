from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_trips_per_route():
    response = client.get("/analytics/trips-per-route")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for item in response.json():
        assert "route_id" in item


def test_busiest_stops():
    response = client.get("/analytics/busiest-stops")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_trips_by_hour():
    response = client.get("/analytics/trips-by-hour")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for item in response.json():
        assert 0 <= item["hour"] <= 23


def test_route_statistics():
    response = client.get("/analytics/routes/77119")

    assert response.status_code == 200

    data = response.json()

    assert data["route_id"] == "77119"
    assert data["total_trips"] == 153
    assert data["stops_served"] == 48
    assert data["average_stops_per_trip"] == 22.5


def test_route_not_found():
    response = client.get("/analytics/routes/132498")

    assert response.status_code == 404
    assert response.json()["detail"] == "Route 132498 not found"


def test_database_health():
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_agencies():
    response = client.get("/agencies")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_routes():
    response = client.get("/routes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_stops():
    response = client.get("/stops")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_trips():
    response = client.get("/trips")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_stop_times():
    response = client.get("/stop-times")

    assert response.status_code == 200
    assert isinstance(response.json(), list)