/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package movement;

import core.Coord;
import core.DTNHost;
import core.Settings;
import core.SimClock;
import core.World;
import movement.map.MapNode;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

/**
 * Map based movement model that uses predetermined paths within the map area.
 * Other than MapRouteMovement, this movement model uses fixed paths to get from one stop to another
 * (no pathfinder). Additionally, a schedule for when each node should arrive at which route stop is respected.
 * See toolkit/smrm/README.md for details and instructions on how to generate needed files.
 */
public class TransitMapMovement extends MapBasedMovement implements
	SwitchableMovement {

	/** Per node group setting used for selecting a route file ({@value}) */
	public static final String ROUTE_FILE_S = "routeFile";

	/** Per node group schedule containing route time information */
	public static final String SCHEDULE_FILE_S = "scheduleFile";

	private TransitControlSystem system;
	private short currentStopIndex;
	private short routeType;
	private double waitTime = 0;
	private TransitTrip currentTrip;
	private int control_system_id; 
	private int number_of_trips_served;

	/**
	 * Creates a new movement model based on a Settings object's settings.
	 * @param settings The Settings object where the settings are read from
	 */
	public TransitMapMovement(Settings settings) {
		super(settings);
		Settings settingsMovement = new Settings(MAP_BASE_MOVEMENT_NS);
		String stopsFile = settings.getSetting(ROUTE_FILE_S);
		String scheduleFile = settings.getSetting(SCHEDULE_FILE_S);
		String mapFile = settingsMovement.getSetting(FILE_S + getOkMapNodeTypes()[0]);

		system = new TransitControlSystem(
				stopsFile,
				scheduleFile,
				mapFile,
                getMap(),
                getOkMapNodeTypes()[0]
        );
		routeType = system.getRouteType();
		//control_system_id = system.getId();
		number_of_trips_served = 0;
	}

	/**
	 * Copyconstructor. Gives a route to the new movement model from the
	 * list of routes and randomizes the starting position.
	 * @param proto The TransitMapMovement prototype
	 */
	protected TransitMapMovement(TransitMapMovement proto) {
		super(proto);
		this.currentStopIndex = proto.currentStopIndex;
		this.system = proto.system;
		this.control_system_id = system.getNewId();
		this.routeType = proto.routeType;
	}

    @Override
    public Path getPath() {
        TransitWay tw = currentTrip.nextWay();
	    tw.adjustSpeed(waitTime);
	    return tw;
    }
    
    /*
	 * Print the vehicle's name, the coordinates of the station it is at, and
	 * the timestamp when a vehicle arrives at a station.
	 */
    public void printArrival(DTNHost host, ArrayList<DTNHost> stations) {
    	double max = -1;
    	Set<Map.Entry<Coord, Double>> entries = host.getLocationsAndTimes().entrySet();
    	
    	/*
    	 * Find the most recent timestamp from before the vehicle stopped at
    	 * its current station and assign it to max.
    	 */
    	if (host.getLocationsAndTimes().size() > 0) {
    		max = Collections.max(host.getLocationsAndTimes().values());
    	}
    	
    	/*
    	 * Find the coordinates of the key that has max as its value. Find the
    	 * station that is closest to these coordinates and print the necessary
    	 * information.
    	 */
    	for (Entry<Coord, Double> entry : entries) {
	    	if (entry.getValue().equals(max)) {
				double entry_x = entry.getKey().getX();
				double entry_y = entry.getKey().getY();
				
				for (DTNHost station : stations) {
					double station_x = station.getLocation().getX();
					double station_y = station.getLocation().getY();
						
					if (Math.abs(entry_x - station_x) < 50 && Math.abs(entry_y - station_y) < 50) {
						System.out.println(host.getName() + " " + station.getLocation() + " " + max);
						host.getLocationsAndTimes().clear();
						return;
					}
				}
			}
    	}
    }

    @Override
	public double nextPathAvailable() {
    	DTNHost host = getHost();
    	ArrayList<DTNHost> stations = World.getStations();
    	
    	/*
    	 * The try-catch handles exceptions that are thrown when printArrival is
    	 * called at the beginning of the simulation, before the world has been
    	 * initialized.
    	 */
    	try {	
			printArrival(host, stations);
		} catch (Exception e) {
			
		}
    	
		if (currentTrip.atFirstStop()) {
			waitTime = 0;
			// Turn of the communication system of mobile devices at initialization
			getHost().setCommunicationSystemON(false);
			return currentTrip.getStartTime();
		}
		if (currentTrip.atLastStop()) {
			currentTrip = system.getTripForStop(
					(int) SimClock.getTime(),
					currentTrip.getCurrentStop(),
					this.control_system_id
			);
//			currentTrip = system.getTripForStop(control_system_id);
			waitTime = 0;
			if (currentTrip == null || currentTrip.getStartTime() - SimClock.getTime() > 1200) {
				getHost().setCommunicationSystemON(false);
			}
			// When no more trips from this stop exist, halt here.
			if (currentTrip == null)
				return Double.MAX_VALUE;
			return currentTrip.getStartTime();
		}
		waitTime = generateWaitTime();
		return SimClock.getTime() + waitTime;
	}

	/**
	 * Returns the first stop on the route
	 */
	@Override
	public Coord getInitialLocation() {
		//currentTrip = system.getInitialTrip((int) SimClock.getTime());
		currentTrip = system.getInitialTrip(control_system_id);
		return currentTrip.startLocation().clone();
	}

	@Override
	public TransitMapMovement replicate() {
		return new TransitMapMovement(this);
	}

	@Override
	protected void checkMapConnectedness(List<MapNode> nodes) {
		// map needs not to be connected, since it is combined out of all route maps
	}
}


