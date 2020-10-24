/* global window */
import React, {useState, useEffect} from 'react';
import {render} from 'react-dom';
import {StaticMap} from 'react-map-gl';
import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {TripsLayer} from '@deck.gl/geo-layers';
import {PathLayer} from '@deck.gl/layers';
import {IconLayer} from '@deck.gl/layers';
import {TextLayer} from '@deck.gl/layers';
import {ScatterplotLayer} from '@deck.gl/layers';

const routes = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/routes.json';
const messages = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/messages.json';
const trips = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/trips.json';
const stops = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/stops.json';
const arrivals = 'https://raw.githubusercontent.com/ebaustria/the-one/master/toolkit/visualization/json_arrays/freiburg1/arrivals.json';
const s_zoom = 12;
const loop_l = 64800;
const trail_l = 120;
const animation_s = 10;
const lon = 7.841710;
const lat = 47.995712;

const MAPBOX_TOKEN = "pk.eyJ1IjoiZXJpY2J1c2giLCJhIjoiY2thcXVzMGszMmJhZjMxcDY2Y2FrdXkwMSJ9.cwBqtbXpWJbtAEGli1AIIg";

const DATA_URL = {
  ROUTES: routes,
  MESSAGES: messages,
  TRIPS: trips,
  STOPS: stops,
  ARRIVALS: arrivals
};

const ICON_MAPPING = {
  marker: {x: 0, y: 0, width: 128, height: 128, mask: true}
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
    new ScatterplotLayer({
      id: 'arrivals',
      data: arrivals,
      radiusScale: 6,
      radiusMinPixels: 0,
      radiusMaxPixels: 100,
      getPosition: d => d.coordinates,
      getRadius: d => isVisible(d.timestamp, this.state.time, 10, 25),
      getFillColor: d => [253, 128, 93],
      getLineColor: d => [0, 0, 0],
      currentTime: this.state.time,
      getTimestamps: d => d.timestamp,
      updateTriggers: {
        getRadius: [d => isVisible(d.timestamp, this.state.time, 10, 25)]
      },
      transitions: {
        getRadius: {
          type: 'spring',
          stiffness: 0.01,
          damping: 0.15,
          duration: 200
        }
      }
    }),
    new PathLayer({
      id: 'routes',
      data: routes,
      widthMinPixels: 3,
      rounded: true,
      getPath: e => e.path,
      getColor: e => e.color, //colorToRGBArray(d.color),
      getWidth: 3
    }),
    new TripsLayer({
      id: 'trips',
      data: trips,
      getPath: d => d.path,
      getTimestamps: d => d.timestamps,
      getColor: [253, 128, 93], //d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
      opacity: 1,
      widthMinPixels: 3,
      rounded: true,
      trailLength,
      currentTime: this.state.time,
      getWidth: 3,
      shadowEnabled: false
    }),
    new IconLayer({
      id: 'stops',
      data: stops,
      pickable: true,
      iconAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
      iconMapping: ICON_MAPPING,
      getIcon: g => 'marker',
      sizeScale: 10,
      getPosition: g => g.coordinates,
      getSize: g => 3,
      getColor: g => g.color,
      getPixelOffset: [0, -12]
    }),
    new TextLayer({
      id: 'messages',
      data: messages,
      getPosition: d => d.coordinates,
      getText: d => d.notification,
      getSize: 16,
      getColor: d => (d.notification === "transfer aborted" ? [255, 0, 0, isVisible(d.timestamp, this.state.time, 30, 255)] : [0, 0, 0, isVisible(d.timestamp, this.state.time, 30, 255)]),
      backgroundColor: [255, 255, 255],
      getTextAnchor: 'middle',
      getAlignmentBaseline: 'top',
      getPixelOffset: [0, 3],
      updateTriggers: {
        getColor: [d => isVisible(d.timestamp, this.state.time, 30, 255)]
      }
      /*
      transitions: {
        getColor: {
          type: 'spring',
          stiffness: 0.01,
          damping: 0.15,
          duration: 20
          //enter: d => [255]
        }
      }
      */
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
