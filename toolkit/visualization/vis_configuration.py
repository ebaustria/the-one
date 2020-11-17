from lib import coord_conversion
from lib import route_conversion
from lib import stop_conversion
from lib import arrival_conversion
from lib import message_conversion
import app_configuration as ac
import sys

local_coords = sys.argv[1]
gps_coords = sys.argv[2]
arrivals = sys.argv[3]
messages = sys.argv[4]
scenario = sys.argv[5]

print("Making trips list...")
trips = coord_conversion.make_trips(local_coords, gps_coords)

print("Making routes list...")
routes = route_conversion.make_routes(gps_coords)

print("Making stops list...")
stops = stop_conversion.make_stops(gps_coords, scenario)

print("Making arrivals list...")
arrivals = arrival_conversion.make_arrivals(arrivals, gps_coords)

print("Making messages list...")
messages = message_conversion.message_json(messages, gps_coords)

with open("toolkit/visualization/app/app.js", 'w') as template:
    ac.write_lines(routes, messages, stops, arrivals, trips, template, scenario)
