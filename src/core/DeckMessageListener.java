package core;

public interface DeckMessageListener {
	
	/**
	 * Tracks locations and timestamps of the messaging activity of DTNHosts.
	 * @param location The location of the DTNHost
	 * @param time The current time of the SimClock
	 * @param action A string describing the action that occurred
	 */
	public void writeMessage(String location, double time, String action);
}
