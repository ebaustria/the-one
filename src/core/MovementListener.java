/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package core;

/**
 * Interface for classes that want to be informed about node movement.
 */
public interface MovementListener {

	/**
	 * Method is called every time a host receives a new destination from its
	 * movement model.
	 * @param host The host that got a new destination
	 * @param destination Coordinates of the destination
	 * @param speed Speed towards that destination
	 */
	public void newDestination(DTNHost host, Coord destination, double speed);

	/**
	 * Method is called when a host receives its initial location from
	 * movement model.
	 * @param host The host that got the location
	 * @param location Coordinates of the location
	 */
	public void initialLocation(DTNHost host, Coord location);
	
	/**
	 * Method is called when a host reaches a waypoint and when a host is leaving
	 * a station.
	 * @param host The host that is at a waypoint
	 * @param location The location of the host
	 * @param time The current time of the SimClock
	 */
	public void atWaypoint(DTNHost host, Coord location, double time);
}
