#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

void create_vector_of_objects(std::ifstream& input,std::vector<std::vector<int>>& vec,int ile_pkt,int d){
    std::string line;
    int i=0;
    while(std::getline(input,line)){
        std::istringstream iss(line);
        std::vector<int> vec2;
        int a;
        while(iss>>a){
            vec2.push_back(a);
        }
        vec.push_back(vec2);
        i++;
    }
    if(i!=ile_pkt){
        std::cout<<"Wrong number of points";
    }
    for(int i=0;i<ile_pkt;i++){
        if(vec[i].size()!=d){
            std::cout<<"Wrong number of dimensions";
        }
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
               }
            }
        else if (a=="-d"){
            std::istringstream iss(argv[i+1]);
            if ((iss>>d)&& iss.eof()){
                    //the number is right
               }
        }


    }

    std::ifstream input(input_file);
    std::ofstream output(output_file);
    std::cout<<7;

    
    
    int ile_pkt =20;
    std::vector<std::vector<int>>vec;
    create_vector_of_objects(input,vec,ile_pkt,d);
    for(int i=0;i<ile_pkt;i++){
        for(int j=0;j<d;j++){
            output<<vec[i][j]<<" ";
        }
        output<<"\n";
    }
    
    
    
    return 0;
    


}
