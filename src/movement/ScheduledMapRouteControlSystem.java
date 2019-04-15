package movement;

import core.Coord;
import core.SettingsError;
import movement.map.MapNode;
import movement.map.SimMap;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class ScheduledMapRouteControlSystem {

	private int routeType;
	private List<Path> pathsForward;
    private List<Path> pathsBackward;
	private int nrofHostsForward = 0;
    private int nrofHostsBackward = 0;
    private ScheduledRouteStop start;
    private ScheduledRouteStop end;
    private short nrofStops;

	private final String COMMA_DELIMITER = ",";
	public final short HOST_DIRECTION_FORWARD = 0;
    public final short HOST_DIRECTION_BACKWARD = 1;


	/**
	 * Creates a new movement model based on a Settings object's settings.
	 */
	ScheduledMapRouteControlSystem(String fileName, SimMap map, int okMapType) {
		pathsForward = new ArrayList<>();
        pathsBackward = new ArrayList<>();
		List<ScheduledRouteStop> stops = readStops(fileName, map);
		start = stops.get(0);
		end = stops.get(stops.size() - 1);
		nrofStops = (short) stops.size();

		buildPaths(stops, okMapType);

	}

	private List<ScheduledRouteStop> readStops(String fileName, SimMap map) {
		boolean mirror = map.isMirrored();
		double xOffset = map.getOffset().getX();
		double yOffset = map.getOffset().getY();

		List<ScheduledRouteStop> stops = new ArrayList<>();
		FileReader fr;
		try {
			fr = new FileReader(fileName);
		} catch (FileNotFoundException e) {
			throw new SettingsError("Cannot find stops file.");
		}
		try (BufferedReader br = new BufferedReader(fr)) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] columns = line.split(COMMA_DELIMITER);
				if (columns.length != 2) {
					throw new SettingsError("Malformed stops file supplied, needs two columns.");
				}
				String[] coords = columns[0].split(" ");
				if (coords.length != 2) {
					throw new SettingsError("Malformed stops file supplied, " +
							"needs two coordinate values, space separated.");
				}
				Coord c = new Coord(
						Double.valueOf(coords[0]),
						Double.valueOf(coords[1])
				);
				if (mirror) {
					c.setLocation(c.getX(), -c.getY());
				}
				c.translate(xOffset, yOffset);

				MapNode node = map.getNodeByCoord(c);
				if (node == null) {
					throw new SettingsError("Stop "+coords[0]+", "+coords[1]+" (transformed: "+
							c.getX()+", "+c.getY()+") is not a valid Map node");
				}

				int timeTo = Integer.parseInt(columns[1]) * 60;
				stops.add(new ScheduledRouteStop(node, timeTo));
			}

		} catch (IOException e) {
			e.printStackTrace();
		} catch (NumberFormatException e2) {
			throw new SettingsError("Malformed stops file supplied, " +
					"first column must be two double values, second column int value");
		}

		return stops;
	}

	private void buildPaths(List<ScheduledRouteStop> stops, int okMapType) {
		int nextStopIdx = 0;
		MapNode currentNode = stops.get(nextStopIdx).node;
		nextStopIdx++;
		MapNode nextStop = stops.get(nextStopIdx).node;
		MapNode endStation = stops.get(stops.size() - 1).node;
		MapNode lastWayPoint = new MapNode(null);
		double distance = 0;
		Path p = new Path();

		nodes:
		while (!currentNode.equals(endStation)) {
			p.addWaypoint(currentNode.getLocation());

			for (MapNode n : currentNode.getNeighbors()) {
				if (n.equals(nextStop)) {
					p.addWaypoint(n.getLocation());
					distance += getDistance(currentNode, n);
					int timeTo = stops.get(nextStopIdx).timeTo;
					p.setSpeed(distance / timeTo);

					pathsForward.add(p);
					distance = 0;
					p = new Path();

					if (!n.equals(endStation)) {
						nextStopIdx++;
						nextStop = stops.get(nextStopIdx).node;
					}
					lastWayPoint = currentNode;
					currentNode = n;
					continue nodes;
				}
				if (!n.equals(lastWayPoint) && n.isType(okMapType)) {
					lastWayPoint = currentNode;
					currentNode = n;
					distance += getDistance(lastWayPoint, currentNode);
					continue nodes;
				}
			}
		}
		buildBackwardsPaths(pathsForward);
	}

	private void buildBackwardsPaths(List<Path> pathsForward) {
	    for (Path p : pathsForward) {
	        List<Coord> coords = new ArrayList<>(p.getCoords());
            Collections.reverse(coords);
            Path p2 = new Path(p.getSpeed());
            for (Coord c : coords) {
                p2.addWaypoint(c);
            }
            pathsBackward.add(p2);
        }
	    Collections.reverse(pathsBackward);
    }

	private double getDistance(MapNode n1, MapNode n2) {
		return n1.getLocation().distance(n2.getLocation());
	}

}