import lib.coord_conversion as cc
from typing import List, Tuple
import json


def message_json(local_coordinates: str, gps_coordinates: str, scenario: str):

    message_timestamps = parse_timestamps(local_coordinates)
    message_gps = cc.gps_list(gps_coordinates)
    message_final_coords = combine_lists(message_timestamps, message_gps)

    dict_list = [single_dictionary(entry) for entry in message_final_coords]

    json_file = json.dumps(dict_list, indent=2)

    with open("json_arrays/" + scenario + "/messages.json", "w") as file:
        file.write(json_file)


def single_dictionary(tup: Tuple[List[float], float, str]):
    new_dict = {}
    new_dict["coordinates"] = tup[0]
    new_dict["timestamp"] = tup[1]
    new_dict["notification"] = tup[2]

    return new_dict


def carried_messages(local_coordinates: str, gps_coordinates: str):
    dict_list = []

    carried_timestamps = cc.timestamps_list(local_coordinates)
    carried_gps = cc.gps_list(gps_coordinates)
    carried_final_coords = cc.final_list(carried_timestamps, carried_gps)

    for name, gps, timestamp, messages in carried_final_coords:
        new_dict = {}
        new_dict["name"] = name
        new_dict["coordinates"] = gps
        new_dict["timestamp"] = timestamp
        new_dict["messages"] = str(messages)

        dict_list.append(new_dict)

    json_file = json.dumps(dict_list, indent=2)

    with open("carried_messages.json", "w") as file:
        file.write(json_file)


def parse_timestamps(local_coordinates: str) -> List[Tuple[Tuple[float, float], float, str]]:

    # Reads file with timestamps into program and stores it as a list of tuples.
    time_coords_1 = []

    with open(local_coordinates, 'r') as time:
        print("    Reading local coordinates and timestamps...")
        reader = time.readlines()
        for row in reader:
            coords_time = row.split()
            x_y_vals = coords_time[0]
            time = coords_time[1]
            action_taken = coords_time[2] + " " + coords_time[3]
            tup = (x_y_vals, time, action_taken)
            time_coords_1.append(tup)

    # Converts the coordinates and timestamps in time_coords_1 from strings to numeric values.
    time_coords_2 = []

    for coords, time, action in time_coords_1:
        time = time.strip(',')
        time = float(time)
        coords = cc.cast_to_float(coords)
        new_tuple = (coords, time, action)
        time_coords_2.append(new_tuple)

    return time_coords_2


# Makes a list of tuples containing the GPS coordinates and timestamps from the two lists passed as parameters. Each
# tuple contains a set of GPS coordinates, a timestamp, and a notification.
def combine_lists(timestamps: List[Tuple[Tuple[float, float], float, str]],
                  coords_list: List[Tuple[Tuple[float, float], List[float]]]) -> List[Tuple[List[float], float, str]]:
    final_coords = []

    print("    Making list of GPS coordinates with timestamps...")
    for coords, timestamp, action in timestamps:
        for local, gps in coords_list:
            if coords == local:
                new = (gps, timestamp, action)
                final_coords.append(new)

    return final_coords
