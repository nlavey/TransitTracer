import pandas as pd


DATA_PATH = "data/raw"


def extract_agency():
    return pd.read_csv(f"{DATA_PATH}/agency.txt")


def extract_routes():
    return pd.read_csv(f"{DATA_PATH}/routes.txt")


def extract_stops():
    return pd.read_csv(f"{DATA_PATH}/stops.txt")


def extract_trips():
    return pd.read_csv(f"{DATA_PATH}/trips.txt")


def extract_stop_times():
    return pd.read_csv(f"{DATA_PATH}/stop_times.txt")