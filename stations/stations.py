import pandas as pd

stations = pd.read_csv('data/stations.csv', delimiter=';', low_memory=False, na_values="nan")
stations_clean = stations[stations["is_suggestable"] == "t"].sort_values(by=["name"])


def get_station_coords(station_slug):
    latitude = stations_clean[stations_clean["slug"] == station_slug].latitude.item()
    longitude = stations_clean[stations_clean["slug"] == station_slug].longitude.item()
    return latitude, longitude


def get_stations_df():
    return stations_clean.copy()


def is_supported_station(station_slug):
    return stations_clean[stations_clean["slug"] == station_slug].shape[0] > 0
