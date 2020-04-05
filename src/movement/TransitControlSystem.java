package movement;

import core.Coord;
import core.SettingsError;
import core.SimError;
import input.WKTMapReader;
import movement.map.MapNode;
import movement.map.SimMap;
import movement.TransitTrip.TripDirection;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

class TransitControlSystem {

	private short routeType;
    private List<TransitStop> stops;
    private volatile TreeMap<Integer, TransitTrip> schedule;
    private Random r;

    /** Type of the route ID: circular ({@value}).
     * After reaching the last node on path, the next node is the first node */
    public static final short CIRCULAR = 1;
    /** Type of the route ID: ping-pong ({@value}).
     * After last node on path, the direction on path is reversed */
    public static final short PINGPONG = 2;

    private final String COMMA_DELIMITER = ",";


	/**
	 * Creates a new movement model based on a Settings object's settings.
	 */
	TransitControlSystem(String stopsFile, String scheduleFile, String nodesFile, SimMap map, long okMapType) {
		stops = readStops(stopsFile, map);
		TransitStop start = stops.get(0);
		TransitStop end = stops.get(stops.size() - 1); // TODO: reference trip may have different end

		if (start.equals(end)) {
		    routeType = CIRCULAR;
        } else {
		    routeType = PINGPONG;
        }

		// construct the reference trip one way
        buildPaths(stops, nodesFile, map, okMapType);
        schedule = readSchedule(scheduleFile);
        r = new Random();
	}
	
	private void updateCoordinate(SimMap map, Coord c) {
		double xOffset = map.getOffset().getX();
		double yOffset = map.getOffset().getY();

		if (map.isMirrored()) {
			c.setLocation(c.getX(), -c.getY());
		}
		c.translate(xOffset, yOffset);

	}

	/**
	 * Read the stop files to have an ordered list of stations
	 * @param fileName
	 * @param map
	 * @return An ordered list of TransitStops
	 */
	private List<TransitStop> readStops(String fileName, SimMap map) {
		List<TransitStop> stops = new ArrayList<>();

		TransitStop previous = null;
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
				updateCoordinate(map, c);

				MapNode node = map.getNodeByCoord(c);
				if (node == null) {
					throw new SettingsError("Stop "+coords[0]+", "+coords[1]+" (transformed: "+
							c.getX()+", "+c.getY()+") is not a valid Map node");
				}

				int timeTo = Integer.parseInt(columns[1]);

				TransitStop next = new TransitStop(node, timeTo);
				next.setPrev(previous);
				if (previous != null) {
					previous.setNext(next);
				}
				previous = next;
				stops.add(next);
			}
			if (stops.size() < 2) {
				throw new SettingsError("Malformed stops file supplied: " + fileName +
						"needs at least 2 stops to run simulation");
			}

		} catch (IOException e) {
			e.printStackTrace();
		} catch (NumberFormatException e2) {
			throw new SettingsError("Malformed stops file supplied: " + fileName +
					"first column must be two double values, second column int value");
		}

		return stops;
	}

	private TreeMap<Integer, TransitTrip> readSchedule(String fileName) {
		TreeMap<Integer, TransitTrip> schedule = new TreeMap<>();
		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
		Date timeStart = null;
		try {
			timeStart = sdf.parse("00:00:00");
		} catch (ParseException e) {
			e.printStackTrace();
		}
		FileReader fr;

		try {
			fr = new FileReader(fileName);
		} catch (FileNotFoundException e) {
			throw new SettingsError("Cannot find schedule file.");
		}
		try (BufferedReader br = new BufferedReader(fr)) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] columns = line.split(COMMA_DELIMITER);
				if (columns.length != 3) {
					throw new SettingsError("Malformed schedule file supplied, needs 3 columns.");
				}

				Date time = sdf.parse(columns[0]);
				long seconds = (time.getTime() - timeStart.getTime()) / 1000;
				int startIndex = Integer.parseInt(columns[1]);
				int endIndex = Integer.parseInt(columns[2]);
				schedule.put((int) seconds, new TransitTrip(
						(int) seconds,
						stops.get(startIndex),
						stops.get(endIndex),
						startIndex < endIndex ?
								TripDirection.FORWARD :
								TripDirection.BACKWARD
				));
			}

			if (schedule.isEmpty()) {
				schedule = null;
			}

		} catch (IOException e) {
			e.printStackTrace();
		} catch (NumberFormatException e) {
			throw new SettingsError("Malformed stops file supplied, " +
					"first column must be two double values, second column int value");
		} catch (java.text.ParseException e) {
			throw new SettingsError("Can not parse time");
		} catch (IndexOutOfBoundsException e) {
			throw new SettingsError("Stop index for trip is out of bounds");
		}

		return schedule;
	}

	
	/**
	 * Read a trip from node files. Return it as an ordered list of nodes
	 * @param fileName
	 * @param map
	 * @return An ordered list of TransitStops
	 */

	List<MapNode> readPath(String nodesFile, List<TransitStop> stops, SimMap map, long okMapType) {
		SimMap mapFromDisk;

		List<MapNode> nodeList = new ArrayList<MapNode>();
		List<Coord> coordList = new ArrayList<Coord>();
		
		WKTMapReader r = new WKTMapReader(true);
		try {
			coordList = r.loadPathAsList(new File(nodesFile), (int)okMapType);
		} catch (IOException e) {
			throw new SimError(e.toString(),e);
		}
		
		for (Coord c: coordList) {
			updateCoordinate(map, c);
			MapNode n = map.getNodeByCoord(c);
			if (n != null) {
				nodeList.add(n);
			} else {
				throw new SettingsError("Stop " + c + " is not a valid Map node");
			}			
		}
		
		MapNode startNode = stops.get(0).node;

		if (!startNode.getLocation().equals(coordList.get(0))) {
			System.out.println("Error - inicial node not found in nodes file.");
			System.exit(1);
		}
		
		MapNode lastNode = stops.get(stops.size()-1).node;
		if (!lastNode.getLocation().equals(coordList.get(coordList.size() - 1))) {
			System.out.println("Error - final node not found in nodes file.");
			System.exit(1);
		}
		
		return nodeList;
	}

	
	/**
	 * 
	 * @param stops
	 * @param map 
	 * @param okMapType
	 * 
	 * Assumes that the order in the nodes file is correct
	 * This is necessary:
	 * 
	 *                 -------------------------
	 * 	              /                         \
	 * X ----------- y ----------- z ----------- w ----------- X
	 *              /                             \
	 *             o                               p
	 *
	 * y is neighbor of X (last hop), z, and w.
	 * A node should not have two neighbors forward... 
	 * The information that w is neighbor due to line o-y-w-p is lost.
	 * 
	 * Solution: assume that the file nodes are ordered and read the
	 * right order direct from file
	 */
	
	private void buildPaths(List<TransitStop> stops, String nodesFile, SimMap map, long okMapType) {
		TransitStop currentStop = stops.get(0);
		TransitStop nextStop = currentStop.getNext();
		MapNode currentNode = currentStop.node;
		MapNode nextStopNode = nextStop.node;
		List<MapNode> orderedPath = readPath(nodesFile, stops, map, okMapType);

		MapNode endNode = stops.get(stops.size() - 1).node; // TODO: when using reference trip, this might not be right. Fix it
		MapNode lastWayPoint = new MapNode(null);
		double distance = 0;
        TransitWay p = new TransitWay();

		//System.out.println("Stop Node:" + currentNode.toString());
		int index = 0;
		
		while (!currentNode.equals(endNode)) {
			p.addWaypoint(currentNode.getLocation());

			MapNode nextNode = orderedPath.get(index+1);
			distance += getDistance(currentNode, nextNode);
			// neighbor is nextStopNode
			if (nextNode.equals(nextStopNode)) {
				p.setDuration(nextStop.timeTo);
				p.setDistance(distance);

				currentStop.setForward(p);
				nextStop.setBackward(p.reversed());

				distance = 0;
				p = new TransitWay();

				if (!nextNode.equals(endNode)) {
					currentStop = nextStop;
					nextStop = nextStop.getNext();
					nextStopNode = nextStop.node;
				}
			}
				
			lastWayPoint = currentNode;
			currentNode = nextNode;
			index += 1;
		}
	}

	private double getDistance(MapNode n1, MapNode n2) {
		return n1.getLocation().distance(n2.getLocation());
	}


    public short getRouteType() {
        return routeType;
    }


    public synchronized TransitTrip getInitialTrip(int time) {
		if (schedule == null) {
			return defaultTrip(time);
		}
		if (schedule.size() == 0)
			throw new SettingsError("There is a host group that has a higher number of hosts than "+
					"trips in the respective schedule. nrofHosts must always be <= count of trips");
		int key = schedule.ceilingKey(time);
		return schedule.remove(key);
	}

	public synchronized TransitTrip getTripForStop(int time, TransitStop currentStop) {
		// Inexistent schedule (possibly bug?)
		if (schedule == null ) {
			System.out.println("Inexistent schedule - BUG");
			return defaultTripForStop(time, currentStop);
		}
		// schedule empty or no more schedules
		else if (schedule.values().isEmpty()) {
			return null;
		}
		Integer key = schedule.ceilingKey(time);
		if (key == null) {
			return null;
		}
		
		try {
			while (!schedule.get(key).getFirstStop().equals(currentStop)) {
				key = schedule.higherKey(key);
				if (key == null)
					return null;
			}
		}
		catch(NullPointerException e) {
			    // do something other
			System.out.println("Oops! Error getting next trip");
		}		
		
			return schedule.remove(key);
	}

	private TransitTrip defaultTrip(int time) {
		if (r.nextBoolean()) {
			return new TransitTrip(
					time,
					stops.get(0),
					stops.get(stops.size()-1),
					TripDirection.FORWARD
			);
		}
		return new TransitTrip(
				time,
				stops.get(stops.size()-1),
				stops.get(0),
				TripDirection.BACKWARD
		);

	}

	private TransitTrip defaultTripForStop(int time, TransitStop currentStop) {
		System.out.println ("WARNING -- default time trip -- error?");
		TransitStop lastStop = currentStop.equals(stops.get(0)) ? stops.get(stops.size()-1) : stops.get(0);
		return new TransitTrip(
				time,
				currentStop,
				lastStop,
				TripDirection.BACKWARD //FIXME!
		);
	}
}

