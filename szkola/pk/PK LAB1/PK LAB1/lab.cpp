#include <iostream>
class czlowiek{
public:
	czlowiek(){}
	virtual void przedstaw_sie()=0;
	virtual char pierwsza_litera()=0;
	virtual void set_name(std::string nowe_imie)=0;
	std::string imie;
private:



};
class lekarz : public czlowiek
{
public:
	lekarz(){}
	void przedstaw_sie() {
		std::cout << imie;
	}
	char pierwsza_litera() {
		return imie[0];
	}
	void  set_name(std::string nowe_imie) override {
		 imie = nowe_imie;
	}
	~lekarz(){}
};
int main() {
	lekarz michal;
	michal.set_name("michal");
	michal.przedstaw_sie();


}