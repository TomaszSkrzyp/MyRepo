#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<random>
void vec(std::vector<int>& vector,int size){
    static std::default_random_engine re{ std::random_device{}() };
    using Dist = std::uniform_int_distribution<int>;
    static Dist uid{};
    for (int i = 0; i < size; i++)
    {
        vector.push_back(uid(re, Dist::param_type{ 0,100 }));
    }


}
int main(){
    int n=20;
    std::vector<int> data;
    vec(data,n);
    std::ofstream dataset;
    dataset.open("dataset.txt");
    if(dataset)
    for(int i=0;i<n;i++){
        dataset<<data[i]<<" ";
        if (i%4==0){
            dataset<<std::endl;
        }
    }
    
   
}