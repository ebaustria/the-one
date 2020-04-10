package movement;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.TreeMap;

import core.SettingsError;
import input.TransitReader;
import movement.TransitTrip.TripDirection;
import movement.map.SimMap;

public class TransitControlSystem {

	private short routeType;
    private List<TransitStop> stops;
    private volatile TreeMap<Integer, ArrayList<TransitTrip>> schedule;

    // tripsPerMobile[mobileId][departure times]
    private ArrayList<LinkedList<TransitTrip>> tripsPerMobile = new ArrayList<LinkedList<TransitTrip>>();
    private Random r;
    private TransitReader t_reader;
    private int device_id;

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
	public TransitControlSystem(String stopsFile, String scheduleFile, String nodesFile, SimMap map, long okMapType) {
		this.t_reader = new TransitReader(stopsFile, scheduleFile, nodesFile, map, okMapType);
		stops = this.t_reader.getStops();
		TransitStop start = stops.get(0);
		TransitStop end = stops.get(stops.size() - 1); // TODO: reference trip may have different end

		if (start.equals(end)) {
		    routeType = CIRCULAR;
        } else {
		    routeType = PINGPONG;
        }

		// read schedule (s) and alternatives to the schedule list
        schedule = this.t_reader.readSchedule();
        setTripsPerVehicle();
        
        // the schedule is distributed over mobile nodes
        r = new Random();
        
        // Device_id is used as identifier to order the trips
        // Every host receives an id that defines the trips it takes part.
        device_id = 0;
	}
	
    public short getRouteType() {
        return routeType;
    }

//    public synchronized TransitTrip getInitialTrip(int time) {
//		if (schedule == null) {
//			return defaultTrip(time);
//		}
//		if (schedule.size() == 0)
//			throw new SettingsError("There is a host group that has a higher number of hosts than "+
//					"trips in the respective schedule. nrofHosts must always be <= count of trips");
//		int key = schedule.ceilingKey(time);
//		// TODO FIXME - just get the first 
//		return schedule.remove(key).get(0);
//	}

    public synchronized TransitTrip getInitialTrip(int dev_id) {
    	if (tripsPerMobile.get(dev_id).size() == 0)
    		return null;
    	return tripsPerMobile.get(dev_id).removeFirst();
	}

    
	public synchronized TransitTrip getTripForStop(int time, TransitStop currentStop, int dev_id) {
    	TransitTrip trip;
    	
    	if (tripsPerMobile.get(dev_id).isEmpty())
    		return null;
		
    	trip = tripsPerMobile.get(dev_id).removeFirst();

		assert (trip.getStartTime() >= time);
    	assert (currentStop.node.getLocation().equals(trip.startLocation()));
		return trip;
	}

//	public synchronized TransitTrip getTripForStop(int control_system_id, TransitStop depart_from) {
//		if (tripsPerMobile.get(control_system_id).isEmpty()) { 
//			return null;
//		}
//		int new_departure_time = tripsPerMobile.get(control_system_id).remove();
//		TransitTrip newTrip = schedule.get(new_departure_time);
//		try {	// find the first possible trip departing from "depart_from" 
//			while (!schedule.get(new_departure).getFirstStop().equals(depart_from)) {
//				new_departure = schedule.higherKey(new_departure);
//				if (new_departure == null)
//					return null;
//			}
//		}
//		catch(NullPointerException e) {
//			    // do something other
//			System.out.println("Oops! Error getting next trip");
//		}		
//		return schedule.remove(new_departure);
//	}
	
//	public synchronized TransitTrip getTripForStopAtSchedule(int depart_after, TransitStop depart_from, TreeMap<Integer,ArrayList<TransitTrip>> localSchedule) {
//
//		if (localSchedule == null ) {
//			assert(false);
//			return defaultTripForStop(depart_after, depart_from);
//		}
//		
//		// Get the next departure time after "depart_after"
//		Integer new_departure = localSchedule.ceilingKey(depart_after);
//
//		if (new_departure == null) { //no further trips to be served
//			return null;
//		}
//		
//		try {	// find the first possible trip departing from "depart_from" 
//			while (!localSchedule.get(new_departure).getFirstStop().equals(depart_from)) {
//				new_departure = localSchedule.higherKey(new_departure);
//				if (new_departure == null)
//					return null;
//			}
//		}
//		catch(NullPointerException e) {
//			    // do something other
//			System.out.println("Oops! Error getting next trip");
//		}		
//		return localSchedule.remove(new_departure);
//	}
	
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
	
	/**
	 * Based on the schedule, define the list of trips that each mobile device may serve.
	 * @return An ordered list of TransitStops
	 */
	private void setTripsPerVehicle() {
	    TreeMap<Integer, ArrayList<TransitTrip>> schedule_copy = (TreeMap<Integer, ArrayList<TransitTrip>>) schedule.clone();
	    int device_int_id = 0;

	    while (!schedule_copy.isEmpty()) {
	    	tripsPerMobile.add(new LinkedList<TransitTrip>());
	    	serve_trips_with_mobile(device_int_id, schedule_copy);
		    device_int_id++;
	    }	
	}
		
	/**
	 * Define all trips a single mobile can take responsibility.
	 * It does not need an inicial station or time, since it will take any available.
	 * @param startTrip: first trip to be served by this vehicle
	 * @param device_id: id to order the vehicle to the trips queue (tripsPerMobile)
	 * @param schedule: shallow copy of the schedule with the remaining trips to be served
	 * @return An ordered list of TransitStops
	 */
	public int serve_trips_with_mobile(int device_id, TreeMap<Integer, ArrayList<TransitTrip>> schedule_copy) {
		
		int num_served_trips=0;
	    int depart_after;
		TransitStop depart_from;
		
		// get the first trip	
		// TODO: after testing, use the original schedule
		TransitTrip currentTrip = pop_from_schedule(-1, null, schedule_copy);
				//schedule_copy.remove(schedule_copy.firstKey());
		
		while (currentTrip != null) {
    		// add trip to the trip list of this vehicle
    		tripsPerMobile.get(device_id).add(currentTrip);		
    		
    		// search the next trip that departs after the arrival of this trip from the arrival station
			depart_after = currentTrip.getArrivalTime();
			depart_from = currentTrip.getLastStop();
    		//currentTrip = getTripForStopAtSchedule(depart_after, depart_from, schedule_copy);
			currentTrip = pop_from_schedule(depart_after, depart_from, schedule_copy);
    	}
		return num_served_trips;
	}
	
	public int getId() {
		return device_id++;
	}
	
	
	/**
	 * Exclude the first entry of the tree after "at_time" departing from station
	 * if the depart station does not matter, from_station=null
	 * @param from_station
	 * @param to_station
	 * @param at_time
	 * @return
	 */
	private TransitTrip pop_from_schedule(int at_time, TransitStop from_station, TreeMap<Integer, ArrayList<TransitTrip>> d_schedule) {
		TransitTrip ttrip = null;
		
		int time = at_time;
		int candidate_index = -1;
		Map.Entry<Integer,ArrayList<TransitTrip>> entry = d_schedule.ceilingEntry(time);
		
		// no more schedules after "at_time"
		if (entry == null) { 
			return null; 
		}
		
		// In the first trip the station does not matter
		// Take the first trip as candidate
		if (from_station == null) {
			candidate_index = 0;
		} else {		
			// this is not the first trip of the vehicle.
			// Find the next available trip departing from station it is currently located
			while (entry != null) {
				// entry.key == departing time, entry.value() List of trips departing at this time.
				candidate_index = get_trip_index(from_station, entry.getValue());
				if (candidate_index != -1) {
					break;
				}
				// no candidate found in this line, try next
				entry = d_schedule.higherEntry(entry.getKey());
			}	
		}
		
		if (entry != null) {
			ttrip = entry.getValue().remove(candidate_index);
			if (entry.getValue().size() == 0) {
				d_schedule.remove(entry.getKey());
			}
		}

		return ttrip;
	}


	/**
	 * Given a list of TransitTrip, return the index of the one that 
	 * departs from location loc
	 * @return
	 */
	private int get_trip_index(TransitStop from_station, ArrayList<TransitTrip> tripList) {
		int counter = 0;
		for (TransitTrip t: tripList) {
			if (t.startLocation().equals(from_station.node.getLocation())) {
				return counter;
			}
			counter++;
		}
		return -1;
	}
}

