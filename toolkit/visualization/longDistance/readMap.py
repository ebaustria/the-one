from typing import Dict
import xml.etree.ElementTree as ET
from lib.project import Projector
from lib import writer
import os
import datetime
from datetime import timedelta
from datetime import datetime
import pprint
import csv


def write_local_and_gps(p: Projector, routes: Dict) -> None:
    main_local_to_gps = set()

    for r_n in routes.keys():
        ns = routes[r_n]['nodes']
        s = routes[r_n]['stops']

        for key, value in sorted(p.local_to_gps.items()):
            if value in ns or value in s:
                main_local_to_gps.add((key, value))

    with open("regiaoSul_gps_coordinates.csv", 'w') as f:
        writer = csv.writer(f)
        for local, gps in sorted(main_local_to_gps):
            writer.writerow([local, gps])


def get_name_from_file(fname):
    return fname.split('.')[0]


pp = pprint.PrettyPrinter(indent=4)
nodes = {}
vis_stops = {}
routes_latlon = {}
routes_xy = {}
stops_xy = {}

points = set()
#os.chdir("/home/jose/Documents/TU-Dresden/Documents/Papers/AdaptiveRouting/lines/")


def calculate_time_in_seconds(day, timestr):
    hora = datetime.strptime(timestr, "%H:%M")
    t = timedelta(day + hora)
    return t.horas, t.minutes%60, t.seconds%60

# For each route:
    # Departure time of each city and duration between each two cities
schedules = {'Planalto-BagePinheiroMachadoPelotas': {
                                            'Bage': {x:['6:00', '7:30', '10:00', '14:00', '16:00', '18:00', '20:00'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'Pinheiro Machado': {x:['7:50', '9:20', '11:50', '15:50', '17:50', '19:50', '21:50'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'waitingTime': {'PinheiroMachado': 30},
                                            'duration': {'Bage - Pinheiro Machado': 80, 'Pinheiro Machado - Pelotas': 100}
             },'Rainha-JaguaraoArroioGrandePelotas': {
                                            'Jaguarao': {x:['6:00', '7:30', '10:00', '14:00', '16:00', '18:00', '20:00'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'Arroio Grande': {x:['7:50', '9:20', '11:50', '15:50', '17:50', '19:50', '21:50'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'waitingTime': {'PinheiroMachado': 30},
                                            'duration': {'Bage - Pinheiro Machado': 80, 'Pinheiro Machado - Pelotas': 100}
             },'Rainha-PelotasArroioGrandeJaguarao': {
                                            'Pelotas': {x:['6:30', '9:30', '11:30', '14:00', '16:00', '18:00', '20:30'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'Arroio Grande': {x:['7:50', '9:20', '11:50', '15:50', '17:50', '19:50', '21:50'] for x in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']},
                                            'waitingTime': {'PinheiroMachado': 30},
                                            'duration': {'Bage - Pinheiro Machado': 80, 'Pinheiro Machado - Pelotas': 100}
             },


}


for fname in ['HervalArroioGrandePelotas.gpx',
              'HervalPedroOsorioPelotas.gpx',
              'BagePinheiroMachadoPelotas.gpx',
              'BagePiratini.gpx',
              'BagePedroOsorioArroioGrandeJaguarao.gpx',
              'ArroioGrandePedroOsorio.gpx',
              'BagePelotas.gpx',
              'BagePiratini.gpx',
              'CangucuPiratini.gpx',
              'HervalPedroOsorio.gpx',
              'JaguaraoPedroOsorio.gpx',
              'PedrasAltasHerval.gpx',
              'PinheiroMachadoPedrasAltas.gpx',
              'PinheiroMachadoPedrasAltasHervalJaguarao.gpx',
              'PiratiniCerrito.gpx',
              'CerritoPedroOsorio.gpx',
              'ArroioGrandePelotas.gpx',
#            'BagePinheiroMachadoPelotas.gpx',
              'CangucuPelotas.gpx',
              'HervalArroioGrande.gpx',
              'HervalArroioGrandePelotas.gpx',
              'JaguaraoArroioGrande.gpx',
              'JaguaraoPelotas.gpx',
              'PedroOsorioPelotas.gpx',
              'PedroOsorioBage.gpx',
              'PelotasPedroOsorioPiratini.gpx',
              'PiratiniPinheiroMachadoviaJoaoSaraiva.gpx',
              'CangucuPiratini.gpx',
              'PiratiniPelotas.gpx',
              'CerritoPassoDasPedrasFaixaPelotas.gpx'
             ]:
# Linhas para Pelotas:
    # Bage - Pinheiro Machado - Pelotas
    # Pedro Osorio - Pelotas
    # Herval - Pedro Osorio - Pelotas
    # Herval - Arroio Grande Pelotas
    # Piratini - Pelotas
    # Cangucu - Pelotas
    # Jaguarao - Arroio Grande - Pelotas

    route_name = get_name_from_file(fname)
    routes_latlon[route_name] = {'stops':[], 'nodes':[]}

    tree = ET.parse(fname)
    root = tree.getroot()

    stops = []
    for child in root.findall('./{http://www.topografix.com/GPX/1/1}wpt'):
        routes_latlon[route_name]['stops'].append((float(child.get('lat')), float(child.get('lon'))))

    for child in root.findall('./{http://www.topografix.com/GPX/1/1}trk/{http://www.topografix.com/GPX/1/1}trkseg/'):
        #print(child.get('lat'), child.get('lon'))

        point = (float(child.get('lat')), float(child.get('lon')))
        routes_latlon[route_name]['nodes'].append(point)
        points.add(point)

proj = Projector(precision=2)
width, height = proj.init_dimensions(points)
        
print(width, height)

# Transform coordinates from lat, lon to x, y
for route_name in routes_latlon.keys():
    routes_xy[route_name], stops_xy[route_name]={}, {}
    routes_xy[route_name]['nodes'] = proj.transform_coords(routes_latlon[route_name]['nodes'])
    routes_xy[route_name]['stops'] = proj.transform_coords(routes_latlon[route_name]['stops'])
    nodes_file = route_name + "_nodes.wkt"
    stops_file = route_name + "_stops.csv"

    #stops_xy[route_name] = [routes_xy[route_name][0],routes_xy[route_name][-1]]
    stops_xy[route_name]['stops'] = [x for x in routes_xy[route_name]['stops']]

    nodes[route_name] = routes_latlon[route_name]['nodes']
    vis_stops[route_name] = routes_latlon[route_name]['stops']

    writer.write_wkt_linestring(coords=routes_xy[route_name]['nodes'], file=nodes_file)
    writer.write_csv_stops(coords=stops_xy[route_name]['stops'], durations=[30 for _ in range(len(stops_xy[route_name]['stops']))], file=stops_file)
#print(routes_xy)

write_local_and_gps(p=proj, routes=routes_latlon)
