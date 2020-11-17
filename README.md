# The ONE

The Opportunistic Network Environment simulator.

For introduction and releases, see [the ONE homepage at GitHub](http://akeranen.github.io/the-one/).

For instructions on how to get started, see [the README](https://github.com/akeranen/the-one/wiki/README).

The [wiki page](https://github.com/akeranen/the-one/wiki) has the latest information.
# Requirements

* Python 3.4+
* cmake
* gcc >= 4.9 (or clang >= 5.0)

# Getting Started

First, clone the necessary repositories:

```
git clone https://github.com/ebaustria/deck.gl.git
git clone https://github.com/ebaustria/the-one.git
git clone --recurse-submodules https://github.com/ad-freiburg/pfaedle
```

Build and install pfaedle:

```
cd pfaedle
mkdir build && cd build
cmake ..
make -j
make install
```

Navigate to ```the-one``` and compile the program:

```
cd ../..
cd the-one
./compile.sh
```

**Note**: If you are using Java 11, you will need to compile the program with ```./compileJava11.sh```. ```the-one/README.txt``` or ```the-one/README.md``` can be consulted for more information on compiling and running the-ONE, if necessary.

In order to visualize public transit in deck.gl, it is necessary to create a file that maps local coordinates (used in the-ONE) to GPS coordinates. There are two ways to do this depending on whether you are visualizing regiaoSul or a short-distance scenario.

# Visualizing Simulations from the-ONE
## regiaoSul

If you are visualizing the regiaoSul scenario, navigate to ```the-one/toolkit/visualization```, create and activate a virtual environment, and install the dependencies:

```
cd toolkit/visualization
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
source .venv/bin/activate
pip install -r requirements.txt
```

Navigate to ```the-one/toolkit/visualization/longDistance``` and run readMap.py:

```
cd longDistance
python3 -m readMap
```

On line 134, ```readMap.py``` writes a file called ```regiaoSul_gps_coordinates.csv```. This file is the mapping of the local coordinates of each node (used in the ONE) to that node's corresponding GPS coordinates.

After creating the mapping of local coordinates to GPS coordinates, navigate to the-one and run the simulation manually:

<pre>
cd ../..
./one.sh <i>your_map</i>_settings.txt
</pre>

## Short-Distance Scenarios

If you want to visualize a short-distance scenario, navigate to ```the-one/toolkit/gtfs```, create the following virtual environment, and install the dependencies. Then, prepare a map for one of the scenarios in ```the-one/toolkit/gtfs/map_definitions``` (e.g. freiburg1 or helsinki1):

<pre>
cd toolkit/gtfs
python3 -m venv --without-pip venv
curl -sS https://bootstrap.pypa.io/get-pip.py | venv/bin/python
source venv/bin/activate
pip install -r requirements.txt
./prepare_map.sh <i>your_map_definition</i>
</pre>

Allow the script to run to completion. In step 3, the script creates the files that are needed to run the simulation with your map, and it will also create a file called <pre><i>your_map</i>_gps_coordinates.csv</pre>

This file contains the mapping of local coordinates to GPS coordinates.

In step 5, the script runs the simulation for your scenario.

**Note**: It may be necessary to remove the flight recorder in order to run the simulation. If this is the case, open ```the-one/one.sh``` and remove ```-XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=myrecording.jfr ``` from the file. Afterwards, it should work. When the simulation is finished, it will write three reports. The lines of the local coordinates report have the following form: DTNHost name, local coordinates, timestamp, messages. The DTNHost name is the name of the DTNHost in question, the local coordinates are a pair of local coordinates used in the ONE, the timestamp is the simulation time at which the DTNHost is located at the local coordinates in question, and the messages are the number of message bundles that DTNHost is carrying. The messaging report has the following form: local coordinates, timestamp, action. The action is a short string that describes the messaging activity of the DTNHost at that timestamp. The lines of the final report consist of local coordinates and timestamps.

## Creating JSON Files

Navigate to the-one and install the dependencies for ```the-one/toolkit/visualization``` if you haven't already and run ```the-one/prepare_vis.sh``` with your scenario name as an argument. Running this shell script will parse the data in each of the four files that have been generated up to this point, and it will use them to write the file ```the-one/toolkit/visualization/app/app.js```. This is the file that will run the visualization in ```deck.gl```.

<pre>
cd ../..
pip install -r toolkit/visualization/requirements.txt
./prepare_vis.sh <i>your_map</i>
</pre>

## Visualizing the Data

After writing ```the-one/toolkit/visualization/app/app.js```, copy this file to ```deck.gl/examples/website/trips```

### Running the Visualization
Navigate to ```deck.gl/examples/website/trips```, install the dependencies, and run the visualization:

```
cd ..
cd deck.gl/examples/website/trips
npm install
npm start
```

https://deck.gl/docs can be consulted for more information, if necessary.

# License
This code is licensed under the MIT license.
