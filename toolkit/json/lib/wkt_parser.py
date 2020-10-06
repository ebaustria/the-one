from typing import List


def parse_wkt_route(nodes: str, coords) -> List[List[float]]:
    list_to_build = []
    nodes = nodes.strip('\n')
    nodes = nodes.strip("LINESTRING ()")
    nodes = nodes.split(',')

    for node in nodes:
        #node = node.strip(')')
        node = node.split()
        node[0] = float(node[0])
        node[1] = float(node[1])
        new_node = (node[0], node[1])
        for local, gps in coords:
            if new_node == local or (new_node[0] == gps[1] and new_node[1] == gps[0]):
                new_node = gps
                list_to_build.append(new_node)
                break

    return list_to_build


def parse_wkt_stops(stops: List[str]) -> List[List[float]]:
    result = []

    for row in stops:
        if row != '\n':
            row = row.strip("POINT (")
            row = row.strip('\n')
            row = row[:-1]
            row = row.split()
            lat = float(row[0])
            lon = float(row[1])
            new_entry = [lat, lon]
            result.append(new_entry)

    return result
