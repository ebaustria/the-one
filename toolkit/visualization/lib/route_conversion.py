from typing import List, Dict
import json
import lib.wkt_parser as wkt
import pprint
import random
import os
import lib.coord_conversion as cc

pp = pprint.PrettyPrinter(indent=4)


def make_color() -> List[int]:
    red = random.randint(50, 256)
    green = random.randint(50, 256)
    blue = random.randint(50, 256)

    if abs(red - green) < 50 or abs(red - blue) < 50 or abs(green - blue) < 50:
        return make_color()

    return [red, green, blue]


def build_route_list(name: str, color: List[int], nodes: List[List[float]], route_list: List[Dict]) -> List[Dict]:

    new_route = {
        "name": name,
        "color": [0, 204, 102],
        "path": nodes
    }

    route_list.append(new_route)

    return route_list


def make_routes(gps_coords: str, scenario: str) -> None:
    route_list = []
    coords = cc.gps_list(gps_coords)

    for filename in os.listdir("toolkit/json/routes"):
        if filename != ".DS_Store":
            with open("toolkit/json/routes/" + filename, 'r') as f:
                nodes = f.read()
                nodes_list = wkt.parse_wkt_route(nodes, coords)
                # color = make_color()
                color = [255, 0, 0]

            route = filename.split('_')
            route = route[0]
            route_list = build_route_list(route, color, nodes_list, route_list)

    routes_json = json.dumps(route_list, indent=2)

    with open("toolkit/json/json_arrays/" + scenario + "/routes.json", "w") as file:
        file.write(routes_json)
