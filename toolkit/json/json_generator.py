from lib import coord_conversion
from lib import route_conversion
from lib import stop_conversion
from lib import arrival_conversion
from lib import message_conversion
import sys

local_coords = sys.argv[1]
gps_coords = sys.argv[2]
arrivals = sys.argv[3]
messages = sys.argv[4]
scenario = sys.argv[5]

print("Making trips JSON...")
coord_conversion.make_trips(local_coords, gps_coords, scenario)

print("Making routes JSON...")
route_conversion.make_routes(gps_coords, scenario)

print("Making stops JSON...")
stop_conversion.make_stops(gps_coords, scenario)

print("Making arrivals JSON...")
arrival_conversion.make_arrivals(arrivals, gps_coords, scenario)

print("Making messages JSON...")
message_conversion.message_json(messages, gps_coords, scenario)

# print("Making carried messages JSON...")
# message_conversion.carried_messages("carried_messages.txt", "gps_coordinates_brazil.csv")
