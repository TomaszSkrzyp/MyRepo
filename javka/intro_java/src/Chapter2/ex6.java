package Chapter2;
import java.util.Scanner;
public class ex6 {
    public static void main(String[] args){
        String full_name;
        String first_name;
        String last_name;
        Scanner scan=new Scanner(System.in);
        System.out.println("Whats your name?");
        full_name=scan.nextLine();

        int space=full_name.indexOf(' ');
        try {
        first_name=full_name.substring(0,space);

             last_name = full_name.substring(space + 1);
        }
        catch(StringIndexOutOfBoundsException a) {
           System.out.println("Give full name WITH spaces");
            main( args);
            return;
        }
        System.out.println("First name: " + first_name + "Last name: " +
                last_name + "Initials: " + first_name.charAt(0) + last_name.charAt(0));

    }
}
