from pathlib import Path
import pandas as pd


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of raw GTFS files
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_gtfs_file(filename):
    """Load a GTFS text file into a pandas DataFrame."""
    filepath = DATA_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Could not find: {filepath}")

    return pd.read_csv(filepath)


def inspect_file(filename):
    """Print basic information about a GTFS file."""
    df = load_gtfs_file(filename)

    print("=" * 60)
    print(f"FILE: {filename}")
    print("=" * 60)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            print(f"  - {column}: {count:,}")

    print("\nFirst 5 rows:")
    print(df.head())

    print()


def main():
    files = [
        "agency.txt",
        "routes.txt",
        "stops.txt",
        "trips.txt",
        "stop_times.txt",
        "calendar.txt",
    ]

    for filename in files:
        inspect_file(filename)


if __name__ == "__main__":
    main()