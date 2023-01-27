import java.util.Random;
import java.io.FileWriter;
/**
 * IE361 Case Study - Group 12
 * Abderrahmane Harkat     2415297
 * Alperen Oktay Şahin     2305373
 * Youssef Nsouli          2487494
 *
 * @author Youssef Nsouli
 */
public class SimulatorSubOptimal
{
    public static void main(int k) throws Exception
    {
        FileWriter writer = new FileWriter("D:\\METU\\METU 5th Semester\\IE361\\Homework\\SuboptimalSimulation.csv", false);
        for (int i = 0; i < k; i++)
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
                float seatPrice = 41 + pricing.nextFloat() * (710 - 41);
                if (customerArrival <= 0.9 && seatsSold < maxSeats && (reservPrice > penaltyRate || seatsSold < maxSeats - overbookTerritory))
                {
                    totalRevenue = totalRevenue + reservPrice;
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
