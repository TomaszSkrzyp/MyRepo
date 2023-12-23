#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "head.h"
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cout << "za malo argumentow";
        return 1;
    }
    if (argc > 11) {
        std::cout << "za duzo argumentow";
        return 1;
    }
    std::string input_file; std::string output_file; int k; int d; int pkt;

    for (int i = 0; i < argc-1; ++i) {
        std::string a = argv[i];
        if (a == "-i") {
            input_file = argv[i + 1];
            
            while (input_file.substr(input_file.length() - 4) != ".txt") {///plik jest nieprawidlowy
                std::cout << "podaj nazwe pliku numer " << i / 2 + 1 << " wraz z rozszerzeniem .txt"<<"\n";
                std::cin >> input_file;

            };            
            i++;
        }
        else if (a == "-o") {
            output_file = argv[i + 1];

            while (output_file.substr(output_file.length() - 4) != ".txt") {///plik jest nieprawidlowy
                std::cout << "podaj nazwe pliku numer " << i / 2 + 1 << " wraz z rozszerzeniem .txt" << "\n";
                std::cin >> output_file;

            };
            i++;
        }
        else   if (a == "-k") {
            std::istringstream iss(argv[i + 1]);
            if ((iss >> k) && iss.eof()) {
                ///the number is right
            }
            else {
                std::cout << "blad w argumencie numer " << i / 2 +1<< " -argument powinien byc liczba";
                return 1;
            }i++;
        }
        else if (a == "-d") {
            std::istringstream iss(argv[i + 1]);
            if ((iss >> d) && iss.eof()) {
                ///the number is right
            }
            else {
                std::cout << "blad w argumencie numer " << i / 2+1 << " -argument powinien byc liczba";
                return 1;
            }
            i++;
        }
        else   if (a == "-pkt") {
            std::istringstream iss(argv[i + 1]);
            if ((iss >> pkt) && iss.eof()) {
                ///the number is right
            }
            else {
                std::cout << "blad w argumencie numer "<<i/2+1<<" -argument powinien byc liczba";
                return 1;
            }
            i++;
        }
    }
    
    
    create_data(pkt, d, input_file);///tworzenie danych
    ///alternatywnie uzyc pliku creator.py aby utworzyc zestaw danych z klastrami
    
    
    std::vector<Point> Points;
    Points = create_vec(input_file);///stworzenie wektora punktow

    std::vector<Point> Centroidy=k_means(&Points,100, k, pkt, d);
    wyjscie(&Points, k, d, output_file);///przekazanie
    /*std::vector<Point>::iterator it;
    for (it = Centroidy.begin(); it<Centroidy.end(); it++) {
        Point x = *it;
        for (int i = 0; i < d; i++) {
            std::cout << x.coordinates[i]<<" ";
        }
        std::cout << "\n";
    }*/
    
    return 0;
}
///.\x64\Debug\FInalny_Projekt.exe -i dataset.txt -o liczby.txt -k 5 -d 2 -pkt 300
//.\FInalny_Projekt\x64\Debug\FInalny_Projekt.exe -i dataset.txt -o liczby.txt -k 3 -d 2 -pkt 30