package Chapter2;

import java.util.Scanner;
//actually ex5
public class ex3 {
    public static void main(String[] args){
        int count;
        System.out.println("How many eggs?");
        Scanner scannin= new Scanner(System.in);
        count=scannin.nextInt();
        System.out.print("You have "+count/144+" grosses");
        count%=144;

        System.out.print(", "+count/12+" dozens");
        count%=12;
        System.out.print(" and "+count+" eggs");



    }
}
