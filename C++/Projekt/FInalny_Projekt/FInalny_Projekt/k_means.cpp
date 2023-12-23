#include<vector>
#include<iostream>
#include<string>
#include<fstream>
#include"head.h"
std::vector<Point> k_means(std::vector<Point>*Points, int powt, int ilosc_k, int ile_pkt, int d ) {
    ///(adres wektora punktow,ilosc powtorzen algorytmu,ilosc clustrow,ilosc punktow)
    std::vector<Point> Centroidy;///wektor przechowujacy centroidy clustrow
    std::vector<Point>::iterator it;
    std::vector<Point>::iterator p_it;
    for (int i = 0; i < ilosc_k; ++i) {
        Centroidy.push_back(Points->at(rand() % ile_pkt));///wybieranie losowych punktow jako centroidy
    }
    for (int powtorzenia = 0; powtorzenia < powt; powtorzenia++) {
        int licznik = 0;
        std::vector<std::vector<double>> srednie_koordynatow;
        std::vector<int> ilosc_punktow_w_clustrze;
        for (it = Centroidy.begin(); it != Centroidy.end(); ++it) {///iteracja przez centroidy
            ilosc_punktow_w_clustrze.push_back(0);
            int numer_clustera = licznik;

            for (p_it = Points->begin(); p_it != Points->end(); ++p_it) {///przydzielanie punktow do clustrow
                Point iterowany_punkt = *p_it;
                Point iterowany_centroid = *it;
                double odleglosc_od_clustra = iterowany_centroid.distance(iterowany_punkt);
                if (odleglosc_od_clustra < iterowany_punkt.minDist) {
                    iterowany_punkt.minDist = odleglosc_od_clustra;
                    iterowany_punkt.cluster = licznik;
                }
                *p_it = iterowany_punkt;
                *it = iterowany_centroid;

            }
            std::vector<double> srednie_koordynatow_clustra;
            for (int wymiar = 0; wymiar < d; wymiar++) {
                srednie_koordynatow_clustra.push_back(0.0);

            }

            srednie_koordynatow.push_back(srednie_koordynatow_clustra);
            licznik += 1;

        }
        //punkty przydzielone



        for (p_it = Points->begin(); p_it != Points->end(); ++p_it) {
            Point podany_punkt = *p_it;
            int numer_clustra = podany_punkt.cluster;
            ilosc_punktow_w_clustrze[numer_clustra] += 1;///zliczanie ilosci punktow w clustrze
            std::vector<double>::iterator it_coord;///iterator koordyantow podanego punktu
            int numer_wspolrzednej = 0;
            for (it_coord = podany_punkt.coordinates.begin(); it_coord != podany_punkt.coordinates.end(); ++it_coord) {
                double wspolrzedna_podanego_punktu = *it_coord;
                srednie_koordynatow[numer_clustra][numer_wspolrzednej] += wspolrzedna_podanego_punktu;///liczenie srednich koordynatow
                numer_wspolrzednej += 1;
                *it_coord = wspolrzedna_podanego_punktu;

            }
        }
        

        for (int numer_klustra = 0; numer_klustra < ilosc_k; numer_klustra++) {
            for (int l = 0; l < d; l++) {
                srednie_koordynatow[numer_klustra][l] = srednie_koordynatow[numer_klustra][l] / ilosc_punktow_w_clustrze[numer_klustra];///obliczanie sredniej wspolrzednych
                                                                                                                                    ///dla kazdego klustra->
            }                                                                                                                           ///wyznaczenie nowych centroidow    
            Centroidy[numer_klustra] = Point(srednie_koordynatow[numer_klustra]);
        }


    }
    return Centroidy;

    
        

    

}