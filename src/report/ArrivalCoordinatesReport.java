package report;

import java.util.LinkedList;

public class ArrivalCoordinatesReport extends Report {
	
	public static LinkedList<String> report;
	
	public ArrivalCoordinatesReport() {
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
	}
}
