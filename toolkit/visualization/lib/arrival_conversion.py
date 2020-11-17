from typing import Tuple, List, Dict
import lib.coord_conversion as cc


def make_arrivals(local_coordinates: str, gps_coordinates: str) -> List[Dict]:

    arrivals_timestamps = timestamps_list(local_coordinates)
    arrivals_gps = cc.gps_list(gps_coordinates)
    arrivals_final_coords = combine_lists(arrivals_timestamps, arrivals_gps)

    dict_list = [single_dictionary(entry) for entry in arrivals_final_coords]

    return dict_list


# Makes a single dictionary that will be stored as an element in the final list
def single_dictionary(tup: Tuple[List[float], float]) -> Dict:
    new_dict = {}
    new_dict["coordinates"] = tup[0]
    new_dict["timestamp"] = tup[1]
    new_dict["color"] = [253, 128, 93]

    return new_dict


def timestamps_list(local_coordinates: str) -> List[Tuple[Tuple[float, float], float]]:

    # Reads file with timestamps into program and stores it as a list of tuples.
    time_coords_1 = []

    with open(local_coordinates, 'r') as time:
        reader = time.readlines()
        for row in reader:
            coords_time = row.split()
            x_y_vals = coords_time[0]
            time = coords_time[1]
            tup = (x_y_vals, time)
            time_coords_1.append(tup)

    # Reformats the coordinates in time_coords_1 and converts them from strings to numeric values.
    return [time_tuple(entry) for entry in time_coords_1]


# Casts elements in the input tuple to floats and returns a new tuple with those elements.
def time_tuple(tup: Tuple[str, str]) -> Tuple[Tuple[float, float], float]:
    coords = cc.cast_to_float(tup[0])
    time = tup[1].strip(',')
    time = float(time)
    return coords, time


# Makes a list of tuples containing the GPS coordinates and timestamps from the two lists passed as parameters. Each
# tuple contains a set of GPS coordinates and a timestamp.
def combine_lists(timestamps: List[Tuple[Tuple[float, float], float]],
               coords_list: List[Tuple[Tuple[float, float], List[float]]]) -> List[Tuple[List[float], float]]:
    final_coords = []

    for coords, timestamp in timestamps:
        for local, gps in coords_list:
            if coords == local:
                new = (gps, timestamp)
                final_coords.append(new)
                break

    return final_coords
