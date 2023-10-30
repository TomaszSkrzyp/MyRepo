#include <iostream>   // biblioteka dla strumieni wejscia/wyjscia (input/output)
#include <fstream>    // biblioteka dla strumieni plikowych (ofstream, ifstream, fstream)
#include <sstream>    // biblioteka dla strumieni napisowych
#include <iomanip> 
void wypisz(std::ostream& s, const std::string& tekst)
{
	s << tekst;
}

int main(){
    const std::string nazwa_pliku{ "moj-plik" };
	{
		std::ofstream plik;                            // output file stream 
		plik.open(nazwa_pliku);
		if (plik) // sprawdzenie, czy plik jest otwarty
		{
			plik << "Szumia jodly na gor szczycie." << std::endl;

			plik.close();
		}
		return 0;
	}

}