#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
/// @brief ta funkcja jest g
int global=17;
void create_vector_with_points(std::vector<std::vector<int>>& vv,std::ifstream& input_file){
    //C++\Projekt\Clust.exe -i dataset.txt -o liczby.txt -k 10 -d 3
    
    std::string line;
    while(std::getline(input_file, line))
        {
    std::stringstream ss(line);
    int i;
    std::vector<int> v;
    while( ss >> i ){ 
        std::cout<<i<<"\n";
       v.push_back(i);}
    vv.push_back(v);
}
    
}
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
    if (argc<4){
        std::cout<<"za malo argumentow";
    }
    /*std::string input_file;std::string output_file;int k;int d;
    
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
                    ///the number is right
               } i++;
            }
        else if (a=="-d"){
            std::istringstream iss(argv[i+1]);
            if ((iss>>d)&& iss.eof()){
                    ///the number is right
               }
            i++;
        }
    }
    std::vector<std::vector<int>> vector;
    std::ifstream input(input_file);
    create_vector_with_points(vector,input);*/
    ///document entity
    /// i love doxygen

    Point p1=Point({1.0,2.0,3.0});
    Point p2 =Point({0.0,0.0,0.0});
    std::cout<<p1.distance(p2);
    return 0;
}
    
    

    
    
    
   
    
    
    

