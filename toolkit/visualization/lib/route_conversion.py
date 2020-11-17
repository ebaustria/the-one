from typing import List, Dict, Union
import lib.wkt_parser as wkt
import pprint
import random
import os
import lib.coord_conversion as cc

pp = pprint.PrettyPrinter(indent=4)


# Generates a random color
def make_color() -> List[int]:
    red = random.randint(50, 256)
    green = random.randint(50, 256)
    blue = random.randint(50, 256)

    if abs(red - green) < 50 or abs(red - blue) < 50 or abs(green - blue) < 50:
        return make_color()

    return [red, green, blue]


# Makes a list of dictionaries
def build_route_list(name: str, color: List[int], nodes: List[List[float]], route_list: List[Dict]) -> List[Dict]:

    new_route = {
        "name": name,
        "color": [0, 204, 102],
        "path": nodes
    }

    route_list.append(new_route)

    return route_list

# Reads linestring route files, parses them, and puts them into a list
def make_routes(gps_coords: str) -> Union[list, List[Dict]]:
    route_list = []
    coords = cc.gps_list(gps_coords)

    for filename in os.listdir("toolkit/visualization/routes"):
        if filename != ".DS_Store":
            with open("toolkit/visualization/routes/" + filename, 'r') as f:
                nodes = f.read()
                nodes_list = wkt.parse_wkt_route(nodes, coords)
                # color = make_color()
                color = [255, 0, 0]

            route = filename.split('_')
            route = route[0]
            route_list = build_route_list(route, color, nodes_list, route_list)

    return route_list
