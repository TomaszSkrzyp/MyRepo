package Chapter2;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.FileWriter;
public class ex7 {
    public static void main(String[] args){
        try{

            File file=new File("testdata.txt");
            if (file.createNewFile());
        }
        catch(IOException e){
            System.out.println(" create ERRROR");

        }
        try{
            FileWriter writing =new FileWriter("testdata.txt");
            writing.write("Joanna\n");
            for(int i=0;i<3;i++) {
                int new_grade=(int)(Math.random()*4)+2;
                writing.write(new_grade+"\n");
            }
            writing.close();
        }
        catch(IOException e){
            System.out.println("write ERRROR");

        }
        try{
            String student_name;
            double avg=0;

            File file=new File("testdata.txt");
            Scanner reader=new Scanner(file);
            student_name=reader.nextLine();

            while (reader.hasNextLine()){
                int val=Integer.parseInt(reader.nextLine());
                avg+=val;


            }
            System.out.print("Average of student "+student_name+" is ");
            System.out.printf("%1.2f",avg/3);

        }
        catch (FileNotFoundException f){
            System.out.println("reading ERRRROR");
        }

    }
}
