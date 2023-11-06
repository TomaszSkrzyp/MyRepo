#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "inb2win.h"


/// @brief ta funkcja jest g

std::vector<Point> create_vector(std::ifstream& input_file){
    std::vector<Point> vv;
    std::string line;
    while(std::getline(input_file, line))
    {
        std::stringstream ss(line);
        double i;
        std::vector<double> v;
        while( ss >> i ){ 
            std::cout<<i<<"\n";
            v.push_back(i);
        }
        vv.push_back(Point(v));
    }

    return vv;
    }
    ///problem z przekazaniem

    //C++\Projekt\Clust.exe -i dataset.txt -o liczby.txt -k 10 -d 3
 
    

struct Point{///@brief struktura punktu 
    std::vector<double> coordinates; 
    int cluster; 
    double minDist; 
    Point(): 
        coordinates(0.0), 
        cluster(-1), 
        minDist(__DBL_MAX__){} 
    Point(std::vector<double> coordinates):///metoda tworzaca punkt
        coordinates(coordinates), 
        cluster(-1), 
        minDist(__DBL_MAX__){} 
    double distance(Point p){ ///funkcja dystanu pomiedzy punktami 
        double sum=0; 
            for(int i=0;i<coordinates.size();++i){ 
            sum+=(coordinates[i]-p.coordinates[i])*(coordinates[i]-p.coordinates[i]); 
            } 
        return sum; 
    } 
};  
    

int main(int argc,char*argv[]){
    create_vec(n, m);
    struct Point{///@brief struktura punktu 
    std::vector<double> coordinates; 
    int cluster; 
    double minDist; 
    Point(): 
        coordinates(0.0), 
        cluster(-1), 
        minDist(__DBL_MAX__){} 
    Point(std::vector<double> coordinates):///metoda tworzaca punkt
        coordinates(coordinates), 
        cluster(-1), 
        minDist(__DBL_MAX__){} 
    double distance(Point p){ ///funkcja dystanu pomiedzy punktami 
        double sum=0; 
            for(int i=0;i<coordinates.size();++i){ 
            sum+=(coordinates[i]-p.coordinates[i])*(coordinates[i]-p.coordinates[i]); 
            } 
        return sum; 
    } 
};  
    if (argc<4){
        std::cout<<"za malo argumentow";
        return 1;
    }
    std::string input_file;std::string output_file;int k;int d;
    
    for (int i=0;i<argc;++i){
        std::string a=argv[i];
        if (a=="-i"){
                input_file=argv[i+1];
                i++;
        }
        else if(a=="-o"){
            output_file=argv[i+1];
            i++;
        }
       else   if(a=="-k"){
               std::istringstream iss(argv[i+1]);
               if ((iss>>k)&& iss.eof()){
                    ///numer jest git
               } i++;
            }
        else if (a=="-d"){
            std::istringstream iss(argv[i+1]);
            if ((iss>>d)&& iss.eof()){
                    ///numer jest git
               }
            i++;
        }
    }
    
    std::istream input(input_file);
    
    ///document entity
    /// i love doxygen
    /*std::vector<Point> Points;
    std::string line;
    while(std::getline(input, line))
    {
        std::stringstream ss(line);
        double i;
        std::vector<double> v;
        while( ss >> i ){ 
            v.push_back(i);
        }
        Points.push_back(Point(v));
    }*/
    std::vector<Point> Points=create_vector(input);
   
    Point p0=Point({1.0,2.0,3.0});
    std::cout<<Points[4].distance(p0);
    
    return 0;
}
    
    

    
    
    
   
    
    
    

