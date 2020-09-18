package core;

public interface DeckMovementListener {

	/**
	 * Tracks host movement. Should be called when a host reaches a waypoint and when a host is leaving
	 * a station.
	 * @param host The host that is at a waypoint
	 * @param location The location of the host
	 * @param time The current time of the SimClock
	 * @param messages The number of messages the node is carrying
	 */
	public void atWaypoint(DTNHost host, String location, double time, int messages);
}
