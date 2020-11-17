import os
from typing import List, Dict


# Determines how far the initial perspective should zoom based on the size of the map
def set_zoom(scen: str) -> str:
    settings_file = str()

    for file_name in os.listdir(os.getcwd()):
        file_sep = file_name.split(sep='_')
        if file_sep[0] == scen:
            settings_file = open(file_name, 'r')

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


# Writes app.js (the main file for running deck.gl visualization) using input data
def write_lines(routes: List[Dict], messages: List[Dict], stops: List[Dict], arrivals: List[Dict], trips: List[Dict],
                temp, scen) -> None:
    if scen != "freiburg1" and scen != "helsinki1" and scen != "regiaoSul":
        raise ValueError("The necessary data for that scenario is not currently available.")

    print("Writing app.js...")
    imports = [
        "import React, {useState, useEffect} from 'react';\n",
        "import {render} from 'react-dom';\n",
        "import {StaticMap} from 'react-map-gl';\n",
        "import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';\n",
        "import DeckGL from '@deck.gl/react';\n",
        "import {PolygonLayer} from '@deck.gl/layers';\n",
        "import {TripsLayer} from '@deck.gl/geo-layers';\n",
        "import {PathLayer} from '@deck.gl/layers';\n",
        "import {IconLayer} from '@deck.gl/layers';\n",
        "import {TextLayer} from '@deck.gl/layers';\n",
        "import {ScatterplotLayer} from '@deck.gl/layers';\n\n"
    ]

    for line in imports:
        temp.write(line)

    temp.write('const MAPBOX_TOKEN = "pk.eyJ1IjoiZXJpY2J1c2giLCJhIjoiY2thcXVzMGszMmJhZjMxcDY2Y2FrdXkwMSJ9.cwBqtbXpWJbtAEGli1AIIg";\n\n')

    temp.write("const r = [\n")

    # Write the input data to the file
    for entry in routes:
        name = '\t\t"name": ' + '"' + str(entry["name"]) + '"' + ',\n'
        color = '\t\t"color": ' + str(entry["color"]) + ',\n'
        path = '\t\t"path": ' + str(entry["path"]) + '\n'
        temp.write("\t{\n")
        temp.write(name)
        temp.write(color)
        temp.write(path)
        temp.write("\t},\n")

    temp.write("];\n\n")

    temp.write("const m = [\n")

    for entry in messages:
        coords = '"coordinates": ' + str(entry["coordinates"]) + ', '
        time = '"timestamp": ' + str(entry["timestamp"]) + ', '
        notification = '"notification": ' + '"' + entry["notification"] + '"'
        temp.write("\t{")
        temp.write(coords)
        temp.write(time)
        temp.write(notification)
        temp.write("},\n")

    temp.write("];\n\n")

    temp.write("const s = [\n")

    for entry in stops:
        name = '"name": ' + '"' + entry["name"] + '"' + ', '
        coords = '"coordinates": ' + str(entry["coordinates"]) + ', '
        color = '"color": ' + str(entry["color"])
        temp.write("\t{")
        temp.write(name)
        temp.write(coords)
        temp.write(color)
        temp.write("},\n")

    temp.write("];\n\n")

    temp.write("const a = [\n")

    for entry in arrivals:
        coords = '"coordinates": ' + str(entry["coordinates"]) + ', '
        time = '"timestamp": ' + str(entry["timestamp"]) + ', '
        color = '"color": ' + str(entry["color"])
        temp.write("\t{")
        temp.write(coords)
        temp.write(time)
        temp.write(color)
        temp.write("},\n")

    temp.write("];\n\n")

    temp.write("const t = [\n")

    for entry in trips:
        vendor = '\t\t"vendor": ' + '"' + str(entry["vendor"]) + '"' + ',\n'
        path = '\t\t"path": ' + str(entry["path"]) + ',\n'
        timestamps = '\t\t"timestamps": ' + str(entry["timestamps"]) + '\n'
        temp.write("\t{\n")
        temp.write(vendor)
        temp.write(path)
        temp.write(timestamps)
        temp.write("\t},\n")

    temp.write("];\n\n")

    # Set the starting zoom
    temp.write("const s_zoom = " + set_zoom(scen) + ";\n")

    # Set the loop length, trail length, and animation speed
    if scen == "freiburg1" or scen == "helsinki1" or scen == "prague1":
        temp.write("const loop_l = 64800;\n")
        temp.write("const trail_l = 120;\n")
        temp.write("const animation_s = 2;\n")
    elif scen == "regiaoSul":
        temp.write("const loop_l = 604800;\n")
        temp.write("const trail_l = 720;\n")
        temp.write("const animation_s = 30;\n")

    # Set the latitude and longitude
    if scen == "freiburg1":
        temp.write("const lon = 7.841710;\n")
        temp.write("const lat = 47.995712;\n\n")
    elif scen == "helsinki1":
        temp.write("const lon = 24.941132;\n")
        temp.write("const lat = 60.168539;\n\n")
    elif scen == "regiaoSul":
        temp.write("const lon = -52.789164;\n")
        temp.write("const lat = -31.832282;\n\n")

    temp.write("const DATA_URL = {\n\tROUTES: r,\n\tMESSAGES: m,\n\tTRIPS: t,\n\tSTOPS: s,\n\tARRIVALS: a\n};\n\n")
    temp.write("const ICON_MAPPING = {\n\tmarker: {x: 0, y: 0, width: 128, height: 128, mask: true}\n};\n\n")
    temp.write("const ambientLight = new AmbientLight({\n\tcolor: [255, 255, 255],\n\tintensity: 1.0\n});\n\n")
    temp.write("const pointLight = new PointLight({\n\tcolor: [255, 255, 255],\n\tintensity: 2.0,\n\tposition: [-74.05, 40.7, 8000]\n});\n\n")
    temp.write("const lightingEffect = new LightingEffect({ambientLight, pointLight});\n\n")
    temp.write("const material = {\n\tambient: 0.1,\n\tdiffuse: 0.6,\n\tshininess: 32,\n\tspecularColor: [60, 64, 70]\n};\n\n")

    default_theme = [
        "const DEFAULT_THEME = {\n",
        "\tbuildingColor: [74, 80, 87],\n",
        "\ttrailColor0: [253, 128, 93],\n",
        "\ttrailColor1: [23, 184, 190],\n",
        "\tmaterial,\n",
        "\teffects: [lightingEffect]\n",
        "};\n\n"
    ]

    for line in default_theme:
        temp.write(line)

    initial_view_state = [
        "const INITIAL_VIEW_STATE = {\n",
        "\tlongitude: lon,\n",
        "\tlatitude: lat,\n",
        "\tzoom: s_zoom,\n",
        "\tpitch: 45,\n",
        "\tbearing: 0\n",
        "};\n\n"
    ]

    for line in initial_view_state:
        temp.write(line)

    temp.write("const landCover = [[[-74.0, 40.7], [-74.02, 40.7], [-74.02, 40.72], [-74.0, 40.72]]];\n\n")

    app = [
        "export default function App({\n",
        "\tstops = DATA_URL.STOPS,\n",
        "\troutes = DATA_URL.ROUTES,\n",
        "\ttrips = DATA_URL.TRIPS,\n",
        "\tarrivals = DATA_URL.ARRIVALS,\n",
        "\tmessages = DATA_URL.MESSAGES,\n",
        "\ttrailLength = trail_l,\n",
        "\tinitialViewState = INITIAL_VIEW_STATE,\n",
        "\tmapStyle = 'mapbox://styles/mapbox/dark-v9',\n",
        "\ttheme = DEFAULT_THEME,\n",
        "\tloopLength = loop_l, // unit corresponds to the timestamp in source data\n",
        "\tanimationSpeed = animation_s\n",
        "}) {\n",
        "\tconst[time, setTime] = useState(0);\n",
        "\tconst[animation] = useState({});\n\n",
        "\tconst animate = () => {\n",
        "\t\tsetTime(t=> (t + animationSpeed) % loopLength);\n",
        "\t\tanimation.id = window.requestAnimationFrame(animate);\n",
        "\t};\n\n",
        "\tuseEffect(\n",
        "\t\t() => {\n",
        "\t\t\tanimation.id = window.requestAnimationFrame(animate);\n",
        "\t\t\treturn () => window.cancelAnimationFrame(animation.id);\n",
        "\t\t},\n",
        "\t\t[animation]\n",
        "\t);\n\n"
    ]

    for line in app:
        temp.write(line)

    temp.write("\tconst layers = [\n")

    ground = [
        "\t\t// This is only needed when using shadow effects\n",
        "\t\tnew PolygonLayer({\n",
        "\t\t\tid: 'ground',\n",
        "\t\t\tdata: landCover,\n",
        "\t\t\tgetPolygon: f => f,\n",
        "\t\t\tstroked: false,\n",
        "\t\t\tgetFillColor: [0, 0, 0, 0]\n",
        "\t\t}),\n"
    ]

    for line in ground:
        temp.write(line)

    # Add the layers
    scatterplot_layer = [
        "\t\tnew ScatterplotLayer({\n",
        "\t\t\tid: 'arrivals',\n",
        "\t\t\tdata: arrivals,\n",
        "\t\t\tradiusScale: 6,\n",
        "\t\t\tradiusMinPixels: 0,\n",
        "\t\t\tradiusMaxPixels: 100,\n",
        "\t\t\tgetPosition: d => d.coordinates,\n",
        "\t\t\tgetRadius: d => isVisible(d.timestamp, time, 10, 25),\n",
        "\t\t\tgetFillColor: d => [253, 128, 93],\n",
        "\t\t\tgetLineColor: d => [0, 0, 0],\n",
        "\t\t\tcurrentTime: time,\n",
        "\t\t\tgetTimestamps: d => d.timestamp,\n",
        "\t\t\tupdateTriggers: {\n",
        "\t\t\t\tgetRadius: [d => isVisible(d.timestamp, time, 10, 25)]\n",
        "\t\t\t},\n",
        "\t\t\ttransitions: {\n",
        "\t\t\t\tgetRadius: {\n",
        "\t\t\t\t\ttype: 'spring',\n",
        "\t\t\t\t\tstiffness: 0.01,\n",
        "\t\t\t\t\tdamping: 0.15,\n",
        "\t\t\t\t\tduration: 200\n",
        "\t\t\t\t}\n",
        "\t\t\t}\n",
        "\t\t}),\n"
    ]

    for line in scatterplot_layer:
        temp.write(line)

    path_layer = [
        "\t\tnew PathLayer({\n",
        "\t\t\tid: 'routes',\n",
        "\t\t\tdata: routes,\n",
        "\t\t\twidthMinPixels: 3,\n",
        "\t\t\trounded: true,\n",
        "\t\t\tgetPath: e => e.path,\n",
        "\t\t\tgetColor: e => e.color, //colorToRGBArray(d.color),\n",
        "\t\t\tgetWidth: 3\n",
        "\t\t}),\n"
    ]

    for line in path_layer:
        temp.write(line)

    trips_layer = [
        "\t\tnew TripsLayer({\n",
        "\t\t\tid: 'trips',\n",
        "\t\t\tdata: trips,\n",
        "\t\t\tgetPath: d => d.path,\n",
        "\t\t\tgetTimestamps: d => d.timestamps,\n",
        "\t\t\tgetColor: [253, 128, 93], //d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),\n",
        "\t\t\topacity: 1,\n",
        "\t\t\twidthMinPixels: 3,\n",
        "\t\t\trounded: true,\n",
        "\t\t\ttrailLength,\n",
        "\t\t\tcurrentTime: time,\n",
        "\t\t\tgetWidth: 3,\n",
        "\t\t\tshadowEnabled: false\n"
        "\t\t}),\n"
    ]

    for line in trips_layer:
        temp.write(line)

    icon_layer = [
        "\t\tnew IconLayer({\n",
        "\t\t\tid: 'stops',\n",
        "\t\t\tdata: stops,\n",
        "\t\t\tpickable: true,\n",
        "\t\t\ticonAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',\n",
        "\t\t\ticonMapping: ICON_MAPPING,\n",
        "\t\t\tgetIcon: g => 'marker',\n",
        "\t\t\tsizeScale: 10,\n",
        "\t\t\tgetPosition: g => g.coordinates,\n",
        "\t\t\tgetSize: g => 3,\n",
        "\t\t\tgetColor: g => g.color,\n",
        "\t\t\tgetPixelOffset: [0, -12]\n",
        "\t\t}),\n"
    ]

    for line in icon_layer:
        temp.write(line)

    message_layer = [
        "\t\tnew TextLayer({\n",
        "\t\t\tid: 'messages',\n",
        "\t\t\tdata: messages,\n",
        "\t\t\tgetPosition: d => d.coordinates,\n",
        "\t\t\tgetText: d => d.notification,\n",
        "\t\t\tgetSize: 16,\n",
        '\t\t\tgetColor: d => (d.notification === "transfer aborted" ? [255, 0, 0, isVisible(d.timestamp, time, 30, 255)] : [0, 0, 0, isVisible(d.timestamp, time, 30, 255)]),\n',
        "\t\t\tbackgroundColor: [255, 255, 255],\n",
        "\t\t\tgetTextAnchor: 'middle',\n",
        "\t\t\tgetAlignmentBaseline: 'top',\n",
        "\t\t\tgetPixelOffset: [0, 3],\n",
        "\t\t\tupdateTriggers: {\n",
        "\t\t\t\tgetColor: [d => isVisible(d.timestamp, time, 30, 255)]\n",
        "\t\t\t}\n",
        "\t\t})\n"
    ]

    for line in message_layer:
        temp.write(line)

    temp.write("\t];\n\n")

    html = [
        "\treturn (\n",
        "\t\t< DeckGL\n",
        "\t\t\tlayers={layers}\n",
        "\t\t\teffects={theme.effects}\n",
        "\t\t\tinitialViewState={initialViewState}\n",
        "\t\t\tcontroller={true}\n",
        "\t\t>\n",
        "\t\t\t< StaticMap\n",
        "\t\t\t\treuseMaps\n",
        "\t\t\t\tmapStyle={mapStyle}\n",
        "\t\t\t\tpreventStyleDiffing={true}\n",
        "\t\t\t\tmapboxApiAccessToken={MAPBOX_TOKEN}\n",
        "\t\t\t/ >\n",
        "\t\t< / DeckGL >\n",
        "\t);\n",
        "}\n\n"
    ]

    for line in html:
        temp.write(line)

    is_visible = [
        "function isVisible(timestamp, current, tolerance, size) {\n",
        "\tif (timestamp <= (current + tolerance) && timestamp >= current) {\n",
        "\t\treturn size;\n",
        "\t}\n",
        "\treturn 0;\n",
        "}\n\n"
    ]

    for line in is_visible:
        temp.write(line)

    render_to_dom = [
        "export function renderToDOM(container) {\n",
        "\trender( < App / >, container);\n",
        "}\n"
    ]

    for line in render_to_dom:
        temp.write(line)
