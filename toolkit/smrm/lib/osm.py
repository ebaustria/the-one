# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from typing import List, Tuple, Union, TextIO

class OsmRoute:
    def __init__(self,
                 name: str,
                 nodes: List[Tuple[float, float]],
                 stops: List[Tuple[float, float]]):

        self.name = name
        self.nodes = nodes
        self.stops = stops

class OsmRouteParser:
    doc = []
    node_index = {}
    way_index = {}

    def __init__(self, markup: Union[str, TextIO]):
        self.doc = BeautifulSoup(markup, 'lxml')
        self.build_indices()

    def build_indices(self):
        self.node_index = {
            node.attrs['id']: node for node in self.doc.find_all('node')
        }
        self.way_index = {
            way.attrs['id']: way for way in self.doc.find_all('way')
        }

    def parse_routes(self) -> List[OsmRoute]:
        relations = self.doc.find_all('relation')
        routes = []
        routes_processed = []

        for r in relations:
            if not self.is_route(r):
                continue
            name = self.rel_name(r)
            ways = self.rel_ways(r)
            stops = self.rel_stops(r)

            if name in routes_processed or len(ways) < 2:
                continue
            if not ways or not stops:
                continue

            print('processing route', name)

            first_stop = self.ref(stops[0])
            way_nodes = self.sort_way_nodes(ways, first_stop)

            waycoords = self.build_waycoords(way_nodes)
            stopcoords = self.build_stopcoords(stops, waycoords)

            waycoords = self.adjust_waycoords(
                waycoords, stopcoords
            )

            if waycoords and stopcoords:
                routes.append(OsmRoute(name, waycoords, stopcoords))
                routes_processed.append(name)

        return routes

    def sort_way_nodes(self, ways: List, first_stop):
        sorted_way_nodes = []
        first_way, index = self.find_first_way(ways, first_stop)
        first_way_nodes = self.way_nodes(first_way)
        if index >= len(first_way_nodes)/2:
            first_way_nodes.reverse()

        connect = first_way_nodes[-1]
        sorted_way_nodes.extend(first_way_nodes)
        ways.remove(first_way)

        while ways:
            for w in ways:
                nodes = self.way_nodes(w)
                if nodes[0] == connect or nodes[-1] == connect:
                    if nodes[-1] == connect:
                        nodes.reverse()

                    connect = nodes[-1]
                    sorted_way_nodes.extend(nodes)
                    ways.remove(w)
                    break
            else:
                break

        return sorted_way_nodes

    def find_first_way(self, ways, first_stop):
        for w in ways:
            nodes = self.way_nodes(w)
            for i, n in enumerate(nodes):
                if self.ref(n) == first_stop:
                    return w, i

    def build_waycoords(self, way_nodes):
        coords = []
        for n in way_nodes:
            c = self.node_to_coord(n)
            if c not in coords:
                coords.append(c)
        return coords

    def build_stopcoords(self, nodes, waycoords):
        coords = []
        for n in nodes:
            c = self.node_to_coord(n)
            if c in waycoords:
                coords.append(c)
        return coords

    def way_nodes(self, way):
        ref = self.ref(way)
        return self.way_index.get(ref).select('nd')

    def node_to_coord(self, n):
        ref = self.ref(n)
        node = self.node_index.get(ref)
        return (
            float(node.attrs['lat']),
            float(node.attrs['lon'])
        )

    def adjust_waycoords(self, waycoords, stopcoords):
        if not waycoords or not stopcoords:
            return []
        waycoords = self.trim_waycoords(waycoords, stopcoords, start=0)
        waycoords = self.trim_waycoords(waycoords, stopcoords, start=-1)
        return waycoords

    @staticmethod
    def trim_waycoords(waycoords, stopcoords, start):
        while waycoords[start] != stopcoords[start]:
            if waycoords[start] in stopcoords:
                print("Incoherent stop node order. Skiping route.")
                return []
            waycoords.pop(start)
            if not waycoords:
                return []
        return waycoords

    @staticmethod
    def correct_node_order(nodes, next_nodes, index):
        if nodes[index] in next_nodes:
            return nodes

        nodes.reverse()
        print('-> reversed way:', nodes[0].parent.attrs['id'])
        if nodes[index] in next_nodes:
            return nodes

        print('! inconsistent way')
        return []

    @staticmethod
    def ref(tag):
        return tag.attrs['ref']

    @staticmethod
    def is_route(r):
        return r.select('tag[k="type"][v="route"]')

    @staticmethod
    def rel_name(r):
        return r.select_one('tag[k="ref"]').attrs.get('v')

    @staticmethod
    def rel_ways(r):
        return r.select('member[type="way"][role=""]')

    @staticmethod
    def rel_stops(r):
        return r.select('member[type="node"][role="stop"]')



