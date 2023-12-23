#include <iostream>   // biblioteka dla strumieni wejscia/wyjscia (input/output)
#include <fstream>    // biblioteka dla strumieni plikowych (ofstream, ifstream, fstream)
#include <sstream>    // biblioteka dla strumieni napisowych
#include <string> 

int main(){
    std::string napis="lubie pisac  w jezyku pradawnym";
	std::size_t pozycja=napis.find_first_of("a");
	std::cout << pozycja << std::endl;
	
	

}