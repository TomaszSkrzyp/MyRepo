#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
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
    
    

int main(int argc,char*argv[]){

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
                    //the number is right
               } i++;
            }
        else if (a=="-d"){
            std::istringstream iss(argv[i+1]);
            if ((iss>>d)&& iss.eof()){
                    //the number is right
               }
            i++;
        }
    }
    std::vector<std::vector<int>> vector;
    std::ifstream input(input_file);
    create_vector_with_points(vector,input);
   
    return 0;
}
    
    

    
    
    
   
    
    
    

