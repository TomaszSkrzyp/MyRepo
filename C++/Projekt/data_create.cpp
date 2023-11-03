#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<random>
void vec(std::vector<int>& vector,int size,int d){
    static std::default_random_engine re{ std::random_device{}() };
    using Dist = std::uniform_int_distribution<int>;
    static Dist uid{};
    for (int i = 0; i < size; i++){
        /*vector.push_back(uid(re, Dist::param_type{ 0,100 }));*/   
        vector.push_back((double)i);
       
}
}
        


int main(){
    int d=3;
    int ile_pkt=20;
    std::vector<int> data;
    vec(data,d*ile_pkt,d);
    std::ofstream dataset;
    dataset.open("dataset.txt");
    if(dataset)
    for(int i=0;i<(int)d*ile_pkt;i++){
        dataset<<data[i]<<" ";
        if (i%d==d-1 && i!=0){
            dataset<<"\n";
        }
    }
    dataset.close();
    
    return 0;   
}
    