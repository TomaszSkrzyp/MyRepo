#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
int main(int argc,char*argv[]){

    std::string input_file;std::string output_file;
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
    }
    std::cout<<input_file<<output_file;
    std::ifstream inf;
    std::ofstream out;
    inf.open(input_file);
    if(inf){
    int val1;int val2;int val3;
    inf>>val1>>val2>>val3;
    std::cout<<val1<<" "<<val2<<" "<<val3;
    }
    else{
        std::cout<<"wtf";
    }
    
    return 0;
}