import sys


def define_constants(scen, d):

    d[13] = "const routes = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/routes.json';\n"
    d[14] = "const messages = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/messages.json';\n"
    d[15] = "const trips = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/trips.json';\n"
    d[16] = "const stops = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/stops.json';\n"
    d[17] = "const arrivals = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/" + scen + "/arrivals.json';\n"

    if scen == 'freiburg1' or scen == 'helsinki1' or scen == 'prague1':
        d[18] = 'const s_zoom = 12;\n'
        d[19] = 'const loop_l = 64800;\n'
        d[20] = 'const trail_l = 120;\n'
        d[21] = 'const animation_s = 10;\n'
    elif scen == 'regiaoSul':
        d[18] = 'const s_zoom = 9;\n'
        d[19] = 'const loop_l = 604800;\n'
        d[20] = 'const trail_l = 720;\n'
        d[21] = 'const animation_s = 30;\n'

    if scen == 'freiburg1':
        d[22] = 'const lon = 7.841710;\n'
        d[23] = 'const lat = 47.995712;\n'
    elif scen == 'helsinki1':
        d[22] = 'const lon = 24.941132;\n'
        d[23] = 'const lat = 60.168539;\n'
    elif scen == 'regiaoSul':
        d[22] = 'const lon = -52.789164;\n'
        d[23] = 'const lat = -31.832282;\n'

    return d


scenario = sys.argv[1]

with open('template/app.js', 'r') as template:
    data = template.readlines()

data = define_constants(scenario, data)

with open('template/app.js', 'w') as template:
    template.writelines(data)
