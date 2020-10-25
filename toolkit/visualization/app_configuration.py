import sys
import os
from typing import List


def set_zoom(scen: str) -> str:
    one = os.path.dirname(os.path.dirname(os.getcwd()))
    settings_file = str()

    for file_name in os.listdir(one):
        file_sep = file_name.split(sep='_')
        if file_sep[0] == scen:
            settings_file = open(one + '/' + file_name, 'r')

    if settings_file == "":
        raise FileNotFoundError("No settings file was found for the following scenario: " + scen)

    settings_data = settings_file.readlines()

    world_size = settings_data[-2]
    world_size = world_size.split()
    world_size.pop(0)
    world_size.pop(0)

    world_size_x = world_size[0].strip(',')
    world_size_y = world_size[1]

    world_size_x = int(world_size_x)
    world_size_y = int(world_size_y)

    if world_size_x > world_size_y:
        dimension = world_size_x
    else:
        dimension = world_size_y

    if dimension in range(5000):
        return "13"
    if dimension in range(5000, 8000):
        return "12.5"
    if dimension in range(8000, 11000):
        return "12"
    if dimension in range(11000, 14000):
        return "11.5"
    if dimension in range(14000, 18000):
        return "11"

    return "9"


def define_constants(scen: str, d: List[str]) -> List[str]:

    if scen != "freiburg1" and scen != "helsinki1" and scen != "regiaoSul":
        raise ValueError("There are not currently any JSON files for that scenario.")

    # Initialize data URLs
    d[15] = "const r = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/routes.json';\n"
    d[16] = "const m = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/messages.json';\n"
    d[17] = "const t = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/trips.json';\n"
    d[18] = "const s = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/stops.json';\n"
    d[19] = "const a = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/arrivals.json';\n"

    # Set the zoom
    d[20] = 'const s_zoom = ' + set_zoom(scen) + ';\n'

    # Set the loop length, trail length, and animation speed
    if scen == "freiburg1" or scen == "helsinki1" or scen == "prague1":
        d[21] = 'const loop_l = 64800;\n'
        d[22] = 'const trail_l = 120;\n'
        d[23] = 'const animation_s = 2;\n'
    elif scen == 'regiaoSul':
        d[21] = 'const loop_l = 604800;\n'
        d[22] = 'const trail_l = 720;\n'
        d[23] = 'const animation_s = 30;\n'

    if scen == 'freiburg1':
        d[24] = 'const lon = 7.841710;\n'
        d[25] = 'const lat = 47.995712;\n'
    elif scen == 'helsinki1':
        d[24] = 'const lon = 24.941132;\n'
        d[25] = 'const lat = 60.168539;\n'
    elif scen == 'regiaoSul':
        d[24] = 'const lon = -52.789164;\n'
        d[25] = 'const lat = -31.832282;\n'

    return d


scenario = sys.argv[1]

with open("template/app.js", 'r') as template:
    data = template.readlines()

data = define_constants(scenario, data)

with open("template/app.js", 'w') as template:
    template.writelines(data)
