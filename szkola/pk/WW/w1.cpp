#include <iostream>
#include <String>
class PoleTekstowe {
	float pozycja[2];
	float rozmiar[2];
public:

	std::string tekst;
	PoleTekstowe(std::string tekst, float pozycjax, float pozycjay, float rozmiarx, float rozmiary)
		: tekst(tekst) { 
		pozycja[0], pozycja[1] = pozycjax, pozycjay;
		rozmiar[0], rozmiar[1] = rozmiarx, rozmiary;
		std::cout << "Stworzono obiekt pole tekstowo w pozycji " << pozycjax << ", " << pozycjay << " , rozmiarze " << rozmiarx << ", " << rozmiary << " oraz tekscie " << tekst << "\n";
	}

	~PoleTekstowe() {
		std::cout << "Destruktor obiektu pole tekstowe zadzialal \n";
	}



};
class Przycisk
{
	float pozycja[2];
	float rozmiar[2];
public:
	std::string tekst;
	Przycisk(std::string tekst, float pozycjax, float pozycjay, float rozmiarx, float rozmiary)
		: tekst(tekst) { // Przypisanie parametru tekst do pola tekst
		pozycja[0], pozycja[1] = pozycjax, pozycjay;
		rozmiar[0], rozmiar[1] = rozmiarx, rozmiary;
		std::cout << "Stworzono obiekt przycisk w pozycji " << pozycjax << ", " << pozycjay << " oraz rozmiarze " << rozmiarx << ", " << rozmiary << " oraz tekscie " << tekst << "\n";
	}

	~Przycisk() {
		std::cout << "Destruktor obiektu przycisk zadzialal \n";
	}




};
class Okno {	
public:
	std::string tytul;
	float rozmiarx;
	float rozmiary;
	static int ilosc_stworzonych;
	static int ilosc_zywych;

	PoleTekstowe* wskaznik_pole;
	Przycisk* wskaznik_przycisk;


	Okno(std::string tytul, float rozmiarx, float rozmiary, PoleTekstowe* pole, Przycisk* przycisk)
		: tytul(tytul), rozmiarx(rozmiarx), rozmiary(rozmiary), wskaznik_pole(pole), wskaznik_przycisk(przycisk) {
		std::cout << "Stworzono okno o tytule " << tytul << " oraz rozmiarze " << rozmiarx << ", " << rozmiary << "\n";
		ilosc_stworzonych++;
		ilosc_zywych++;
	}

	~Okno() {
		std::cout << "Destruktor obiektu okno zadzialal " << "\n";
		delete wskaznik_pole;
		delete wskaznik_przycisk;
		ilosc_zywych--;
	}
	static int liczba_stworzonych() {
		return ilosc_stworzonych;
	}
	static int liczba_zywych() {
		return ilosc_zywych;
	}


};
int Okno::ilosc_stworzonych = 0;
int Okno::ilosc_zywych = 0;







int main() {
	PoleTekstowe* info = new PoleTekstowe("informacje", 10, 11, 12, 13);
	Przycisk* n = new Przycisk("anuluj", 10, 11, 12, 13);

	Okno* o = new Okno("sport", 12, 13, info, n);
	


	std::cout << o->liczba_stworzonych() << " " << o->liczba_zywych() << "\n";
	std::cout << o->wskaznik_pole->tekst << "\n";

	delete o;
	
	return 0;
}

