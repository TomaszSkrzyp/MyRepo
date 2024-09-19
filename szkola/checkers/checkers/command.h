#pragma once
#include "board.h"

#include <thread>
#include <chrono>  
/**
 * obiekt sluzacy do obslugi wyjscia jak i wejscia
 */
class command_control {
	
	std::list<move*> list;///lista mozliwych ruchow
//
	std::string players[2];/// "imiona" zawodnikow bioracych udzial w grze. przechowywane w tablicy stringow
	char turn;/// informacja o obecnej turze, 'w' oznacza ture bialych, 'b' oznacza ture czarnych
	/// <summary>
	/// funkcja sprawdzajaca czy podany ruch jest legalny. sprawdza rowniez "skoki" o dlugosci jeden bedace czescia dluzszej sekwencji skokow. jesli ruch znajduje sie w liscie ruchow
	/// zwraca "true". 
	/// </summary>
	/// <param name="keys"> lista kluczy zawierajacyh informacje o skoku. funcja aktualizuje te liste w przypadku dluzszej sekwencji skokow</param>
	/// <param name="xs"> wpolrzedna x pola startowego </param>
	/// <param name="ys"> wpolrzedna y pola startowego </param>
	/// <param name="xj"> wpolrzedna x przeskakiwanego pola </param>
	/// <param name="yj"> wpolrzedna y przeskakiwanego pola </param>
	/// <param name="xf"> wpolrzedna x pola koncowego </param>
	/// <param name="yf"> wpolrzedna y pola koncowego </param>
	/// <param name="answer"> wskaznik do praidlowego  ruchu , przekazywany przez referencje co pozwala "zwracac" prawidlowy ruch </param>
	/// <param name="reset"> informacja o koniecznosci zresetowania funckji pobierania ruchu od uzytkowanika </param>
	/// <returns> "true" lub "false" w zaleznosci od tego czy znalezlismy prawidlowy ruch </returns>
	bool one_move_request(std::list<int>& keys, int& xs, int& ys, int& xj, int& yj, int& xf, int& yf,move* & answer,bool &reset);
	/// <summary>
	/// Fukcja pobiera pole od uzytkownika w postaci pozycji na planszy i konwertuje do wartosci int bedacej indeksem
	/// </summary>
	/// <param name="x"> wspolrzedna x pola. pobierana jako referncja z uwagi na potrzebe zaktualizowania wartosci przekonwerowanej </param>
	/// <param name="y"> wspolrzedna y pola. pobierana jako referncja z uwagi na potrzebe zaktualizowania wartosci przekonwerowanej </param>
	void get_pos_from_command(int& x, int& y);
	/// <summary>
	/// funckaja wyswetlajaca ruch w postaci zgodnej z pozycjami na planszy. 
	/// </summary>
	/// <param name="v">wskaznik do ruchu ktory chcemy wyswietlic </param>
	void print_single_move(move* v)const;
	/// <summary>
	/// funckcja "zmazujaca" n lini z terminalu
	/// </summary>
	/// <param name="n_lines"> ilosc lini do "zmazania" </param>
	void clear_lines(int n_lines)const;
	/// <summary>
	/// funckcja ustalajaca wspolrzedna y przeskakiwanego pola. przez kompresje planszy nie jest to trywialne zadanie. wspolrzedna x jest zawsze srednia arytmetyczna xs i xf
	/// </summary>
	/// <param name="yj"> wpolrzedna y przeskakiwanego pola. pozyskiwana przez referencje </param>
	/// <param name="xs"> wpolrzedna x pola startowego </param>
	/// <param name="ys"> wpolrzedna y pola startowego </param>
	/// <param name="yf"> wpolrzedna y pola koncowego </param> 
	void find_y_jumped(int& yj, int xs, int ys, int yf);
	/// <summary>
	/// funkcja ustalajaca wartosc klucza dla skoku. wartosc ta zawiera informacje o punkcie startowym, przeskakiwanym i koncowym
	/// </summary>
	/// <param name="xs"></param>
	/// <param name="ys"></param>
	/// <param name="xj"></param>
	/// <param name="yj"></param>
	/// <param name="xf"></param>
	/// <param name="yf"></param>
	/// <returns></returns>
	int hashed_jump(int xs, int ys, int xj, int yj, int xf, int yf);
	int rev_hash(int i);
	
	
public:	
	
	
	command_control(char t, const std::string& p1,const std::string& p2):turn(t) {
		players[0] = p1; players[1] = p2;
	} 
	~command_control() {

		while (!list.empty()) {
			list.pop_front();
		}

	}
	void move_strength(int cur_score, int score_after) const;
	
	move* move_request();
	void start_game()const;
	void start_round(int score, char turn)const;
	void mid_round(move * m, char turn)const;
	bool end_game(bool is_draw, int index);
	void this_move_command(move* m)const;
	void print_table(const board*b)const;
	void replace_moves(const std::list<move*>& new_list,char t);
	void print_move()const;
	void replace_turn(char t) {
		turn = t;
	}
	char get_turn()const  {
		return turn;
	}
	std::string get_string() const;
};