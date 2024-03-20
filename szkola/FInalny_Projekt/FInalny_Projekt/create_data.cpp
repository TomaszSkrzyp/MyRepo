#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<random>
#include "head.h"
void create_data(int ile_pkt, int d, std::string input_file) {
    std::ofstream dataset;
    dataset.open(input_file);
    if (dataset) {
        static std::default_random_engine re{ std::random_device{}() };
        using Dist = std::uniform_real_distribution<double>;
        static Dist uid{};
        for (int i = 0; i < ile_pkt; i++) {
            for (int l = 0; l < d; l++) {
                dataset << uid(re, Dist::param_type{ 0,100 }) << " ";


            }
            dataset << "\n";
        }

    }

    dataset.close();


}