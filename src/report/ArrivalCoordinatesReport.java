package report;

import core.ArrivalListener;

public class ArrivalCoordinatesReport extends Report implements ArrivalListener {
	
	public ArrivalCoordinatesReport() {
		init();
	}
	
	protected void init() {
		super.init();
	}

	@Override
	public void atStop(String location, double time) {
		write(location + " " + time);
	}
}
