import java.util.*;

public class IRNDCG{
	public static void main(String [] args){
	ArrayList<Integer> relevance = new ArrayList<>(); // stops at the N value
	// add relevance values in order of ranking
	Scanner keyboard = new Scanner(System.in);
	System.out.print("Enter N value: "); int N = keyboard.nextInt(); 
	System.out.println("Enter N relevance values:");
	for(int a = 0; a < N; a++){
		int rel = keyboard.nextInt();
		relevance.add(rel);	
	}
		
	double DCG = 0; 
	int j = 1;

	// DCG value
	for(int i = 0; i < relevance.size(); i++)
	{
		DCG = DCG + (relevance.get(i)/(Math.log(j+1) / Math.log(2)));
		j = j + 1;
	}
	System.out.println("DCG value:" + DCG);

	// IDCG value...sort to ideal order.
	Collections.sort(relevance);
	Collections.reverse(relevance);
	System.out.println("Ideal order" + relevance);
	double IDCG = 0; 
	int k = 1;
	for(int i = 0; i < relevance.size(); i++)
	{
		IDCG = IDCG + (relevance.get(i)/(Math.log(k+1) / Math.log(2)));
		k = k + 1;
	}
	System.out.println("IDCG value:" + IDCG);

	// NDCG value
	double NDCG = DCG / IDCG;
	System.out.println("NDCG value:" + NDCG);
	}
}


