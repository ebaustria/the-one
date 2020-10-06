package report;

import java.util.LinkedList;

public class MessageCoordinatesReport extends Report {
	
	public static LinkedList<String> report;
	
	public MessageCoordinatesReport() {
		report = new LinkedList<String>();
		init();
	}
	
	protected void init() {
		super.init();
	}
	
	@Override
	public void done() {
		for (String s : report) {
			write(s);
		}
		super.done();
	}
}
