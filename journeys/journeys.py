import json
import requests
from stations import get_station_coords

source_file = 'data/journeys.json'

with open(source_file) as json_file:
    journeys = json.load(json_file)


def save_to_json(data):
    with open(source_file, 'w') as file:
        json.dump(data, file, indent=4)


def get_journey_slug(slug_1, slug_2):
    slug = slug_1 + '_TO_' + slug_2
    return slug


def sort_stations(station_1, station_2):
    if station_1 < station_2:
        return station_1, station_2
    else:
        return station_2, station_1


def import_line(origin_slug, destination_slug):
    origin_lat, origin_lon = get_station_coords(origin_slug)
    origin_coords = f"{origin_lat},{origin_lon}"
    destination_lat, destination_lon = get_station_coords(destination_slug)
    destination_coords = f"{destination_lat},{destination_lon}"

    call_URL = f"https://trainmap.ntag.fr/api/route?dep={origin_coords}&arr={destination_coords}&simplify=1 "
    call = requests.get(call_URL, timeout=360).json()
    line = call["geometry"]["coordinates"][0]
    return line


def new_line(station_1, station_2):
    journey_slug = get_journey_slug(station_1, station_2)
    line = import_line(station_1, station_2)
    journeys[journey_slug] = line
    save_to_json(journeys)
    return line


def get_line(station_1, station_2):
    station_1, station_2 = sort_stations(station_1, station_2)
    journey_slug = get_journey_slug(station_1, station_2)
    if journey_slug in journeys.keys():
        line = journeys[journey_slug]
    else:
        line = new_line(station_1, station_2)
    return line
