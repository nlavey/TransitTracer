from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load(filename):
    """Load a GTFS file."""
    return pd.read_csv(DATA_DIR / filename)


def main():
    routes = load("routes.txt")
    trips = load("trips.txt")
    stops = load("stops.txt")
    stop_times = load("stop_times.txt")

    print("GTFS RELATIONSHIPS")
    print("=" * 60)

    # Routes -> Trips
    trips_per_route = trips.groupby("route_id").size()

    print("\nTrips per route:")
    print(trips_per_route.head())

    # Trips -> Stop Times
    stops_per_trip = stop_times.groupby("trip_id").size()

    print("\nStops per trip:")
    print(stops_per_trip.head())

    # Stops -> Stop Times
    stop_usage = stop_times.groupby("stop_id").size()

    print("\nMost frequently referenced stops:")
    print(stop_usage.sort_values(ascending=False).head(10))

    # Basic counts
    print("\nDataset counts:")
    print(f"Routes:     {len(routes):,}")
    print(f"Trips:      {len(trips):,}")
    print(f"Stops:      {len(stops):,}")
    print(f"Stop times: {len(stop_times):,}")


if __name__ == "__main__":
    main()