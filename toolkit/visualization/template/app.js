/* global window */
import React, {useState, useEffect} from 'react';
import {render} from 'react-dom';
import {StaticMap} from 'react-map-gl';
import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {TripsLayer} from '@deck.gl/geo-layers';

const routes = "https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/routes.json";
const messages = "https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/messages.json";
const trips = "https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/trips.json";
const stops = "https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/stops.json";
const arrivals = "https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/arrivals.json";
const s_zoom = 12;
const loop_l = 64800;
const trail_l = 120;
const animation_s = 30;
const lon = 7.841710;
const lat = 47.995712;

const DATA_URL = {
  ROUTES: routes,
  MESSAGES: messages,
  TRIPS: trips,
  STOPS: stops,
  ARRIVALS: arrivals
};

const ambientLight = new AmbientLight({
  color: [255, 255, 255],
  intensity: 1.0
});

const pointLight = new PointLight({
  color: [255, 255, 255],
  intensity: 2.0,
  position: [-74.05, 40.7, 8000]
});

const lightingEffect = new LightingEffect({ambientLight, pointLight});

const material = {
  ambient: 0.1,
  diffuse: 0.6,
  shininess: 32,
  specularColor: [60, 64, 70]
};

const DEFAULT_THEME = {
  buildingColor: [74, 80, 87],
  trailColor0: [253, 128, 93],
  trailColor1: [23, 184, 190],
  material,
  effects: [lightingEffect]
};

const INITIAL_VIEW_STATE = {
  longitude: lon,
  latitude: lat,
  zoom: s_zoom,
  pitch: 45,
  bearing: 0
};

const landCover = [[[-74.0, 40.7], [-74.02, 40.7], [-74.02, 40.72], [-74.0, 40.72]]];

export default function App({
  buildings = DATA_URL.BUILDINGS,
  trips = DATA_URL.TRIPS,
  trailLength = trail_l,
  initialViewState = INITIAL_VIEW_STATE,
  mapStyle = 'mapbox://styles/mapbox/dark-v9',
  theme = DEFAULT_THEME,
  loopLength = loop_l, // unit corresponds to the timestamp in source data
  animationSpeed = animation_s
}) {
  const [time, setTime] = useState(0);
  const [animation] = useState({});

  const animate = () => {
    setTime(t => (t + animationSpeed) % loopLength);
    animation.id = window.requestAnimationFrame(animate);
  };

  useEffect(
    () => {
      animation.id = window.requestAnimationFrame(animate);
      return () => window.cancelAnimationFrame(animation.id);
    },
    [animation]
  );

  const layers = [
    // This is only needed when using shadow effects
    new PolygonLayer({
      id: 'ground',
      data: landCover,
      getPolygon: f => f,
      stroked: false,
      getFillColor: [0, 0, 0, 0]
    }),
    new TripsLayer({
      id: 'trips',
      data: trips,
      getPath: d => d.path,
      getTimestamps: d => d.timestamps,
      getColor: [253, 128, 93],
      opacity: 1,
      widthMinPixels: 3,
      rounded: true,
      trailLength,
      currentTime: time,
      getWidth: 3,
      shadowEnabled: false
    }),
    new PolygonLayer({
      id: 'buildings',
      data: buildings,
      extruded: true,
      wireframe: false,
      opacity: 0.5,
      getPolygon: f => f.polygon,
      getElevation: f => f.height,
      getFillColor: theme.buildingColor,
      material: theme.material
    })
  ];

  return (
    <DeckGL
      layers={layers}
      effects={theme.effects}
      initialViewState={initialViewState}
      controller={true}
    >
      <StaticMap
        reuseMaps
        mapStyle={mapStyle}
        preventStyleDiffing={true}
        mapboxApiAccessToken={MAPBOX_TOKEN}
      />
    </DeckGL>
  );
}

function isVisible(timestamp, current, tolerance, size) {
  if (timestamp <= (current + tolerance) && timestamp >= current) {
    return size;
  }
  return 0;
}

export function renderToDOM(container) {
  render(<App />, container);
}
