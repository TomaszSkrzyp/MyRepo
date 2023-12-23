
#pragma once
#include<string>
#include <cmath>
void create_data(int ile_pkt, int d, std::string input_file);
struct Point {///@brief struktura punktu 
    std::vector<double> coordinates;
    int cluster;///numer przydzielonego clustera
    double minDist;
    Point(std::vector<double> coordinates) ://lista inicjalizujaca  punktu
        coordinates(coordinates),
        cluster(-1),
        minDist(DBL_MAX) {}
    double distance(Point p) { ///metoda dystanu pomiedzy punktami 
        double sum = 0;
        for (int i = 0; i < coordinates.size(); ++i) {
            sum += (coordinates[i] - p.coordinates[i]) * (coordinates[i] - p.coordinates[i]);
        }
        return sqrt(sum);
    }
};
std::vector<Point>k_means(std::vector<Point>* Points, int powt, int ilosc_k, int ile_pkt, int d);
std::vector<Point> create_vec(std::string input_file);
void wyjscie(std::vector<Point>* Points, int ilosc_k, int d, std::string output_file);
