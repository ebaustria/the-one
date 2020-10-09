#!/bin/sh
set -e

RSUL="regiaoSul"
LOCAL_REPORT=$1_LocalCoordinatesReport.txt
GPS_MAP=$1_gps_coordinates.csv
ARRIVAL_REPORT=$1_ArrivalCoordinatesReport.txt
MESSAGES_REPORT=$1_MessageCoordinatesReport.txt

LOCAL_COORDS=reports/$LOCAL_REPORT
ARRIVALS=reports/$ARRIVAL_REPORT
MESSAGES=reports/$MESSAGES_REPORT

if [ $1 = "$RSUL" ]; then
  GPS_COORDS=toolkit/json/longDistance/$GPS_MAP
else
  GPS_COORDS=toolkit/gtfs/$GPS_MAP
fi

STATIONS=data/$1/stations.wkt
CITIES=data/$1/cities.wkt

rm -rf toolkit/json/routes/*
rm -rf toolkit/json/stops/*
sudo cp data/$1/*_nodes.wkt toolkit/json/routes/
sudo cp $STATIONS toolkit/json/stops/

if test -f "$CITIES"; then
  sudo cp $CITIES toolkit/json/stops/
fi

#Might not be necessary?
mkdir -p toolkit/json/json_arrays/$1

chmod u+x toolkit/json/json_generator.py

python3 toolkit/json/json_generator.py $LOCAL_COORDS $GPS_COORDS $ARRIVALS $MESSAGES $1
