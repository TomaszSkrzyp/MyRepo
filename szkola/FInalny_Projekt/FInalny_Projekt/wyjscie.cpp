#include<fstream>
#include<vector>
#include"head.h"
void wyjscie(std::vector<Point>* Points, int ilosc_k, int d, std::string output_file) {
	std::ofstream strumien_wyjscia(output_file);
	std::vector<std::vector<double>> podzial(ilosc_k);
	std::vector<Point>::iterator it;
	for (it = Points->begin(); it < Points->end(); it++) {
		Point punkt = *it;
		for (double z : punkt.coordinates)
			podzial[punkt.cluster].push_back(z);
	}
	for (int i = 0; i < ilosc_k; i++) {
		strumien_wyjscia << "Kluster " << i << "\n";
		int l = 0;
		for (double wspolrzedna : podzial[i]) {
			strumien_wyjscia << wspolrzedna << " ";
			l += 1;
			if (l % d == 0)
				strumien_wyjscia << "\n";


		}
	}
}