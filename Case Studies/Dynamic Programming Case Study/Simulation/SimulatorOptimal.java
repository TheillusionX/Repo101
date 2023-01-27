import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Random;
import java.io.File;
import java.io.FileWriter;
/**
 * IE361 Case Study - Group 12
 * Abderrahmane Harkat     2415297
 * Alperen Oktay Şahin     2305373
 * Youssef Nsouli          2487494
 *
 * @author Youssef Nsouli
 */
public class SimulatorOptimal
{
    public static void main(int times) throws Exception
    {
        List<String[]> optimalPrices = new ArrayList<String[]>();
        Scanner in = new Scanner(new File("D:\\METU\\METU 5th Semester\\IE361\\Homework\\Optimal_Prices_Continuous.xlsx"));
        in.useDelimiter(",");
        while (in.hasNextLine())
        {
            optimalPrices.add((in.nextLine().split(",")));
        }
        optimalPrices.remove(0);
        FileWriter writer = new FileWriter("D:\\METU\\METU 5th Semester\\IE361\\Homework\\OptimalSimulation.csv", false);
        for (int i = 0; i < times; i++)
        {
            int maxSeats = 100;
            int startTime = 144;
            int overbookTerritory = 10;
            int penaltyRate = 200;
            
            Random arriv = new Random();
            Random rPrice = new Random();
            Random pricing = new Random();
            float totalRevenue = 0.0f;
            int seatsSold = 0;
            for (int t = startTime; t > 0; t--)
            {
                float customerArrival = arriv.nextFloat();
                float reservPrice = 41 + rPrice.nextFloat() * (710 - 41);
                float seatPrice = Float.valueOf(optimalPrices.get(maxSeats - seatsSold)[t]);
                if (customerArrival <= 0.9 && seatsSold < maxSeats && seatPrice < reservPrice)
                {
                    totalRevenue = totalRevenue + seatPrice;
                    seatsSold++;
                }
            }
            if (seatsSold >= maxSeats - overbookTerritory)
            {
                totalRevenue = totalRevenue - penaltyRate * (maxSeats - overbookTerritory);
            }
            writer.write("$" + Float.toString(totalRevenue) + "," + Integer.toString(seatsSold) + "\n");
        }
        writer.close();
    }
}
