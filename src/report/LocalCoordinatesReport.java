package report;

import core.DTNHost;
import core.DeckMovementListener;

public class LocalCoordinatesReport extends Report implements DeckMovementListener {
	
	public LocalCoordinatesReport() {
		init();
	}
	
	protected void init() {
		super.init();
	}
	
	@Override
	public void atWaypoint(DTNHost host, String location, double time, int messages) {
		setPrefix(host.getName());
		write(" " + location + " " + time + " " + messages);
	}
}
