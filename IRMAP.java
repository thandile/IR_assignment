import java.util.*;

public class IRMAP{

	public static void main(String [] args){
		ArrayList<Double> relevance = new ArrayList<>(); // stops at the N value
		ArrayList<Double> precision = new ArrayList<>(); 
		// Add relevance values
		Scanner keyboard = new Scanner(System.in);
		System.out.print("Enter N value: "); 
		int N = keyboard.nextInt(); 
		System.out.println("Enter N relevance values:");
		// add revevance values to arraylist
		for(int a = 0; a < N; a++){
			int rel = keyboard.nextInt(); // should be 0, 1 or 2
			double actualRel = rel/2.0;
			System.out.println(actualRel);
			relevance.add(actualRel);
		}

		// get precisions at each point
		double relCount = 0; 	
		double precisionValue = 0;
		for(int a = 0; a < N; a++){
			relCount = relCount + relevance.get(a);
			System.out.println("Total relevance at " + (a+1) + ": " + relCount);
			
			precisionValue = relCount/(a+1);
			System.out.println("Total precision at " + (a+1) + ": " +precisionValue);
			
			precision.add(precisionValue);			
		}

		// find the sum and average
		double sum = 0;	
		for(double element : precision){
			sum = sum + element;
		}
		double map = sum/(precision.size());
		System.out.println("The MAP value " + map);
	}
}
