package core;

public interface ArrivalListener {
	
	/**
	 * Tracks arrivals at stops. Should be called when a host arrives at a stop.
	 * @param location The location of the DTNHost
	 * @param time The current time of the SimClock
	 */
	public void atStop(String location, double time);
}
