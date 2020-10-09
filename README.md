# The ONE

The Opportunistic Network Environment simulator.

For introduction and releases, see [the ONE homepage at GitHub](http://akeranen.github.io/the-one/).

For instructions on how to get started, see [the README](https://github.com/akeranen/the-one/wiki/README).

The [wiki page](https://github.com/akeranen/the-one/wiki) has the latest information.

# Visualizing Simulations from the-ONE

First, clone the necessary repositories:

```
git clone https://github.com/ebaustria/deck.gl.git
git clone https://github.com/ebaustria/the-one.git
```

Navigate to ```the-one``` and compile the program:

```
cd the-one
./compile.sh
```

**Note**: If you are using Java 11, you will need to compile the program with ```./compileJava11.sh```. ```the-one/README.txt``` or ```the-one/README.md``` can be consulted for more information on compiling and running the-ONE, if necessary.

In order to visualize public transit in deck.gl, it is necessary to create a file that maps local coordinates (used in the-ONE) to GPS coordinates. There are two ways to do this depending on whether you are visualizing regiaoSul or a short-distance scenario.

## regiaoSul

If you are visualizing the regiaoSul scenario, navigate to ```the-one/toolkit/json```, create and activate a virtual environment, and install the dependencies:

```
cd toolkit/json
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
source .venv/bin/activate
pip install -r requirements.txt
```

Navigate to ```the-one/toolkit/json/longDistance``` and run readMap.py:

```
cd longDistance
python3 -m readMap
```

On line 134, ```readMap.py``` writes a file called ```regiaoSul_gps_coordinates.csv```. This file is the mapping of the local coordinates of each node (used in the ONE) to that node's corresponding GPS coordinates.

## Short-Distance Scenarios

Navigate to ```the-one/toolkit/gtfs``` and prepare a map for one of the scenarios in ```the-one/toolkit/gtfs/map_definitions```:

<pre>
cd toolkit/gtfs
./prepare_map.sh <i>your_map_definition</i>
</pre>

Next, navigate to the map you just created, create the GTFS files for the map, navigate to the output directory, and compress the files into a zip drive:

<pre>
cd maps/<i>your_map</i>
pfaedle -D -m tram -x ./<i>your_map</i>.osm .
cd gtfs-out
zip <i>your_map</i>.zip *
</pre>

Navigate back to ```the-one/toolkit/gtfs```, create a virtual environment, install the dependencies, and run ```scenario.py``` using the zip drive you just made as an argument:

<pre>
cd ..
cd ..
cd ..
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
source .venv/bin/activate
pip install -r requirements.txt
python3 scenario.py -t 0 maps/<i>your_map</i>/gtfs-out/<i>your_map</i>.zip
</pre>

Running ```scenario.py``` creates the files that are needed to run the simulation with your map, and it will also create a file called <pre><i>your_map</i>_gps_coordinates.csv</pre>

This file contains the mapping of local coordinates to GPS coordinates.

## Running the-ONE

After creating the mapping of local coordinates to GPS coordinates, navigate to the-one and run the simulation:

<pre>
cd
cd <i>your_path_to</i>/the-one
./one.sh <i>your_map</i>_settings.txt
</pre>

**Note**: It may be necessary to remove the flight recorder in order to run the simulation. If this is the case, open ```the-one/one.sh``` and remove ```-XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=myrecording.jfr ``` from the file. Afterwards, it should work. When the simulation is finished, it will write three reports. The lines of one of the reports have the following form: DTNHost name, local coordinates, timestamp, messages. The DTNHost name is the name of the DTNHost in question, the local coordinates are a pair of local coordinates used in the ONE, the timestamp is the simulation time at which the DTNHost is located at the local coordinates in question, and the messages are the number of message bundles that DTNHost is carrying. One of the other reports has the following form: local coordinates, timestamp, action. The action is a short string that describes the messaging activity of the DTNHost at that timestamp. The lines of the final report consist of local coordinates and timestamps.

## Creating JSON Files

While still in the-one, run ```prepare_json.sh``` with your scenario name as an argument. Running this shell script will parse the data in each of the four files that have been generated up to this point, and it will use them to create five JSON files that can be used for visualization in ```deck.gl```.

<pre>
./prepare_json.sh <i>your_map</i>
</pre>

## Visualizing the Data

Create a remote repository and add it if you haven't already. Stage the five JSON files from the previous section to be committed, commit them, and push them to your remote:

<pre>
git remote add <i>remote_name</i> https://github.com/<i>user</i>/<i>repo</i>.git
git add toolkit/json/json_arrays/<i>your_map</i>/trips.json
git add toolkit/json/json_arrays/<i>your_map</i>/routes.json
git add toolkit/json/json_arrays/<i>your_map</i>/stops.json
git add toolkit/json/json_arrays/<i>your_map</i>/arrivals.json
git add toolkit/json/json_arrays/<i>your_map</i>/messages.json
git commit -m "<i>message</i>"
git push <i>remote_name</i> master
</pre>

deck.gl uses special classes called layers to visualize datasets. Each layer class produces a different effect. In this visualization, we use five different layers: TripsLayer, PathLayer, IconLayer, ScatterplotLayer, and TextLayer. Each of the JSON files we've created needs to be passed to one of these layers so they can be visualized.

Open deck.gl/examples/website/trips/app.js. We need to modify app.js to get it to visualize our data.

**Note**: Functioning versions of app.js are located in ```the-one/toolkit/json/examples``` and can be consulted for examples. If you would like to skip the rest of this section, you should be able to navigate to deck.gl/examples/website/trips and replace the version of app.js that is located there with one of the versions of app.js that is located in the-one. Once you have replaced app.js you can continue with these steps starting at "Running the Visualization".

First, make sure the necessary layer classes are imported at the top of the file:

```
import {TripsLayer} from '@deck.gl/geo-layers';
import {PathLayer} from '@deck.gl/layers';
import {IconLayer} from '@deck.gl/layers';
import {TextLayer} from '@deck.gl/layers';
import {ScatterplotLayer} from '@deck.gl/layers';
```

You will need a mapbox token to see the base map. Create a mapbox token at https://www.mapbox.com/ if you don't already have one and set the token in ```app.js``` directly beneath the imports:

<pre>
const MAPBOX_TOKEN = "<i>your_mapbox_token</i>";
</pre>

**Note**: Be sure to enclose the mapbox token in quotes.

Next, we need to provide the raw data URLs of our JSON arrays to ```app.js```. We will define constant references to the raw data URLs within the ```DATA_URL``` constant. Open the raw data for each JSON file in the remote GitHub repository you have set up and assign each raw data URL as a string to a constant in ```DATA_URL```. For example, you might define the constant reference to ```trips.json``` as:

```
TRIPS: 'https://raw.githubusercontent.com/ebaustria/regiaoSul/master/trips.json'
```

In general, ```DATA_URL``` and the constants defined within it should have the following structure:

<pre>
const DATA_URL = {
  <i>CONST_NAME</i>: 'https://raw.githubusercontent.com/<i>your_github_profile</i>/<i>your_remote_repository</i>/<i>branch</i>/<i>your_data.json</i>',
  ...
};
</pre>

**Note**: Do not forget to add commas in between constant references.

Scroll down to ```export default function App```. At the beginning of the function, use the previously defined constant references to define variables to pass to each layer instance:

<pre>
export default function App({
  <i>data_variable</i> = DATA_URL.<i>CONST_NAME</i>,
  ...
</pre>

The final step is to initialize each layer instance in the ```layer``` constant and provide its respective properties. The correspondence between the datasets and the layers is as follows:

* trips.json --> TripsLayer
* routes_brazil.json --> PathLayer
* stops.json --> IconLayer
* arrivals.json --> ScatterplotLayer
* messages.json --> TextLayer

The following sections provide examples of how to initialize the necessary layers within ```layer```, as well as some additional information.

### TripsLayer
```app.js``` already includes an instance of TripsLayer that can be used in the visualization with minimal changes:

```
    new TripsLayer({
      id: 'trips',
      data: trips,
      getPath: d => d.path,              //do not edit
      getTimestamps: d => d.timestamps,  //do not edit
      getColor: [253, 128, 93],
      opacity: 1,
      widthMinPixels: 3,
      rounded: true,
      trailLength,                       //do not edit
      currentTime: time,                 //do not edit
      getWidth: 3,
      shadowEnabled: false
    }),
```

**Note**: ```data:``` is the property that determines which dataset the layer uses. Every layer needs to be provided with a data property.

The name that is assigned to ```data:``` should correspond to one of the URL variables you defined in the ```App``` function. ```trips``` is passed to the data property of TripsLayer by default. If you gave the constant reference that corresponds to ```trips.json``` a different name in ```App```, make sure you pass that name to the data property instead of ```trips```.

### PathLayer
The general template for the PathLayer's properties is:

<pre>
    new PathLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      widthMinPixels: 3,    //deck.gl will not render a path thinner than 3 pixels no matter how far the user zooms out
      rounded: true,
      getPath: e => e.path,   //do not edit
      getColor: e => e.color,  //do not edit
      getWidth: 3           //the width of each path in meters
    }),
</pre>

**Note**: The ordering of the layer initializations within ```layer``` seems to affect the visibility of some layers. For this reason, it is best to initialize the PathLayer **before** you initialize the TripsLayer in your code.

### IconLayer
The general template for the IconLayer's properties is:

<pre>
    new IconLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      iconAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',   //do not edit
      iconMapping: ICON_MAPPING,  //do not edit
      getIcon: g => 'marker',     //do not edit
      sizeScale: 10,
      getPosition: g => g.coordinates,  //do not edit
      getSize: g => 3,
      getColor: g => g.color,           //do not edit
      getPixelOffset: [0, -10]          //offsets the icon 10 pixels upward
    }),
</pre>

Also make sure to add the following lines below ```DATA_URL```:

```
const ICON_MAPPING = {
  marker: {x: 0, y: 0, width: 128, height: 128, mask: true}
};
```

### ScatterplotLayer
The general template for the ScatterplotLayer's properties is:

<pre>
    new ScatterplotLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      radiusScale: 6,
      radiusMinPixels: 0,     //the minimum circle radius in pixels that deck.gl will display
      radiusMaxPixels: 100,   //the maximum circle radius in pixels that deck.gl will display
      getPosition: d => d.coordinates,                         //do not edit
      getRadius: d => isVisible(d.timestamp, time, 70, 600),   //only edit last two parameters in function call
      getFillColor: d => [253, 128, 93],
      updateTriggers: {
        getRadius: [d => isVisible(d.timestamp, time, 70, 600)]   //only edit last two parameters in function call
      },
      transitions: {
        getRadius: {
          type: 'spring',     //do not edit
          stiffness: 0.01,
          damping: 0.15,
          duration: 100,
          enter: d => [0]     //do not edit
        }
      }
    }),
</pre>

### TextLayer
The general template for the TextLayer's properties is:

<pre>
    new TextLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      getPosition: d => d.coordinates,    //do not edit
      getText: d => d.notification,       //do not edit
      getSize: 16,
      getColor: d => [0, 0, 0, isVisible(d.timestamp, time, 30, 255)],     //only edit last two parameters in function call
      backgroundColor: [255, 255, 255],
      getTextAnchor: 'middle',            //determines where the text is displayed relative to the object's position ('start', 'middle', or 'end')
      getAlignmentBaseline: 'top',     //determines where the text is displayed relative to the object's position ('top', 'center', or 'bottom')
      getPixelOffset: [0, 3],
      updateTriggers: {
        getColor: [d => [0, 0, 0, isVisible(d.timestamp, time, 30, 255)]]  //only edit last two parameters in function call
      }
    }),
</pre>

**Note**: Layer IDs must be unique.

**Note**: Each of the layers presented here has additional properties that have not been included in any of the above code samples. The information provided here is only intended to help users create a working visualization. https://deck.gl/docs/api-reference/layers can be consulted for more information on deck.gl's layers, their properties, and how to modify them.

## Running the Visualization
Navigate to ```deck.gl/examples/website/trips```, install the dependencies, and run the visualization:

```
cd ..
cd deck.gl/examples/website/trips
npm install
npm start
```

https://deck.gl/docs can be consulted for more information, if necessary.

## License
This code is licensed under the MIT license.
