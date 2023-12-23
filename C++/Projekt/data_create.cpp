#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<random>
#include "C:\Users\Dell\source\repos\MyRepo\C++\proj\proj\x64\Debug\create.h"
void create_data(int ile_pkt,int d) {
    std::string destin="dataset.txt";
    
    std::ofstream dataset;
    dataset.open(destin);
    if (dataset)
        static std::default_random_engine re{ std::random_device{}() };
    using Dist = std::uniform_int_distribution<int>;
    static Dist uid{};
    for (int i = 0; i < ile_pkt; i++) {
        /*vector.push_back(uid(re, Dist::param_type{ 0,100 }));*/
        for (int l = 0; l < d; ++l) {
            dataset << l << " ";
        }
        dataset << "\n";
    }

    dataset.close();


}


