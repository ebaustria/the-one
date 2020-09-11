package report;

import core.Coord;
import core.DTNHost;
import core.MovementListener;

public class LocalCoordinatesReport extends Report implements MovementListener {
	
	public LocalCoordinatesReport() {
		init();
	}
	
	protected void init() {
		super.init();
	}

	@Override
	public void newDestination(DTNHost host, Coord destination, double speed) {
		return;
	}

	@Override
	public void initialLocation(DTNHost host, Coord location) {
		return;
	}

	@Override
	public void atWaypoint(DTNHost host, String location, double time) {
		setPrefix(host.getName());
		write(" " + location + " " + time);
	}
}
