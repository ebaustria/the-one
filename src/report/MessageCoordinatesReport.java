package report;

import core.DeckMessageListener;

public class MessageCoordinatesReport extends Report implements DeckMessageListener {
	
	public MessageCoordinatesReport() {
		init();
	}
	
	protected void init() {
		super.init();
	}

	@Override
	public void writeMessage(String location, double time, String action) {
		write(location + " " + time + " " + action);
	}
}
