from typing import List, Dict
import lib.coord_conversion as cc
import lib.wkt_parser as wkt
from os import path


# Makes a list of dictionaries
def build_list(stops: List[List[float]], color: List[int], json_list: List[Dict]) -> List[Dict]:

    for coord in stops:
        new_station = {
            "name": "stop name",
            "coordinates": coord,
            "color": color
        }
        json_list.append(new_station)

    return json_list


# Reads stop files, parses the data, and puts it into a list
def make_stops(gps_coordinates: str, scenario: str) -> List[Dict]:

    result = []
    stations_list = []
    cities = []
    cities_list = []
    coords_list = cc.gps_list(gps_coordinates)

    with open("toolkit/visualization/stops/stations.wkt", 'r') as stations:
        stations = stations.readlines()
        stations = wkt.parse_wkt_stops(stations)

    if path.exists("data/" + scenario + "/cities.wkt"):
        with open("toolkit/visualization/stops/cities.wkt", 'r') as cities:
            cities = cities.readlines()
            cities = wkt.parse_wkt_stops(cities)

    for local, gps in coords_list:
        for station in stations:
            if local[0] == station[0] and local[1] == station[1]:
                stations_list.append(gps)
        for city in cities:
            if local[0] == city[0] and local[1] == city[1]:
                cities_list.append(gps)

    result = build_list(stations_list, [0, 255, 255], result)
    result = build_list(cities_list, [255, 0, 0], result)

    return result
