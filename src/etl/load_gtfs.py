from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/raw")


FILES = [
    "agency.txt",
    "calendar.txt",
    "routes.txt",
    "shapes.txt",
    "stops.txt",
    "stop_times.txt",
    "trips.txt",
]


def load_gtfs_data():
    data = {}

    for filename in FILES:
        filepath = DATA_DIR / filename

        if not filepath.exists():
            raise FileNotFoundError(
                f"Missing GTFS file: {filepath}"
            )

        table_name = filepath.stem
        data[table_name] = pd.read_csv(filepath)

        print(
            f"Loaded {filename}: "
            f"{len(data[table_name])} rows"
        )

    return data

def validate_data(data):
    required_columns = {
        "routes": ["route_id", "route_short_name"],
        "stops": ["stop_id", "stop_name", "stop_lat", "stop_lon"],
        "trips": ["route_id", "service_id", "trip_id"],
        "stop_times": ["trip_id", "stop_id", "arrival_time", "departure_time"],
    }

    for table, columns in required_columns.items():
        df = data[table]

        for column in columns:
            if column not in df.columns:
                print(
                    f"WARNING: {table} is missing {column}"
                )

if __name__ == "__main__":
    data = load_gtfs_data()
    validate_data(data)