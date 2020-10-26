from typing import List, Tuple, Dict
import json


def make_trips(local_coordinates: str, gps_coordinates: str, scenario: str) -> None:

    timestamps = timestamps_list(local_coordinates)
    coords_list = gps_list(gps_coordinates)
    final_coords = final_list(timestamps, coords_list)

    # Makes dictionary out of data from final_coords. Coordinates and timestamps are mapped to vehicle names.
    new_dict = {}
    for name, coords, timestamp, messages in final_coords:
        if name not in new_dict.keys():
            new_dict[name] = []
        new_entry = (coords, timestamp)
        new_dict[name].append(new_entry)

    # Converts each key-value pair from new_dict into a dictionary and adds each dictionary to a list.
    print("    Making final list of dictionaries...")
    json_list = []
    for name in new_dict.keys():
        new_json = {
            "vendor": name,
            "path": [],
            "timestamps": []
        }

        for coords, timestamp in new_dict[name]:
            new_json["path"].append(coords)
            new_json["timestamps"].append(timestamp)

        json_list.append(new_json)

    write_json(json_list, scenario)


def gps_list(gps_coordinates: str) -> List[Tuple[Tuple[float, float], List[float]]]:

    # Reads file with GPS coordinates into program and stores it as a list of tuples.
    coords_list_1 = []

    with open(gps_coordinates, 'r') as coordinates:
        print("    Making list of local-GPS tuples...")
        splt_char = ','
        n = 2
        reader = coordinates.readlines()
        for row in reader:
            row = row.replace(" ", "")
            row = row.replace('"', "")
            row = row.replace('\n', "")
            l = row.split(splt_char)
            new_coords = splt_char.join(l[:n]), splt_char.join(l[n:])
            entry = (new_coords[0], new_coords[1])
            coords_list_1.append(entry)

    # Reformat the data and convert it back to numeric values.
    return [gps_tuple(entry) for entry in coords_list_1]


def gps_tuple(tup: Tuple[str, str]) -> Tuple[Tuple[float, float], List[float]]:
    coords = cast_to_float(tup[0])
    gps = cast_to_float(tup[1])
    gps = [gps[1], gps[0]]
    return coords, gps


def timestamps_list(local_coordinates: str) -> List[Tuple[str, Tuple[float, float], float, int]]:

    # Reads file with timestamps into program and stores it as a list of tuples.
    time_coords_1 = []

    with open(local_coordinates, 'r') as time:
        print("    Reading local coordinates and timestamps...")
        reader = time.readlines()
        for row in reader:
            coords_time = row.split()
            name = coords_time[0]
            x_y_vals = coords_time[1]
            time = coords_time[2]
            messages = coords_time[3]
            tup = (name, x_y_vals, time, messages)
            time_coords_1.append(tup)

    # Reformats the coordinates in time_coords_1 and converts them from strings to numeric values.
    return [time_tuple(entry) for entry in time_coords_1]


def time_tuple(tup: Tuple[str, str, str, str]) -> Tuple[str, Tuple[float, float], float, int]:
    coords = cast_to_float(tup[1])
    time = tup[2].strip(',')
    time = float(time)
    messages = int(tup[3])
    return tup[0], coords, time, messages


# Makes a list of tuples containing the GPS coordinates and timestamps from the two lists passed as parameters. Each
# tuple contains a name, a set of GPS coordinates and a timestamp.
def final_list(timestamps: List[Tuple[str, Tuple[float, float], float, int]],
               coords_list: List[Tuple[Tuple[float, float], List[float]]]) -> List[Tuple[str, List[float], float, int]]:
    final_coords = []

    print("    Making list of GPS coordinates with timestamps...")
    for name, coords, timestamp, messages in timestamps:
        for local, gps in coords_list:
            if coords == local:
                new = (name, gps, timestamp, messages)
                final_coords.append(new)
                break

    return final_coords


# Converts a tuple of strings to a tuple of floats.
def cast_to_float(coords: str) -> Tuple[float, float]:

    coords = coords[1:-1]
    coords = coords.split(',')
    x = float(coords[0])
    y = float(coords[1])
    new_coords = (x, y)

    return new_coords


# Writes the list of dictionaries to a JSON file.
def write_json(json_list: List[Dict], scenario: str) -> None:

    json_file = json.dumps(json_list, indent=2)

    with open("toolkit/visualization/json_arrays/" + scenario + "/trips.json", "w") as file:
        file.write(json_file)
