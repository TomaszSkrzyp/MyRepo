#pragma once
#include "board.h"
class command_control {
	std::string command_in;
	std::string command_out;
	std::list<move*> list;
	char turn;
	bool one_move_request(std::list<int>& keys, int& xs, int& ys, int& xj, int& yj, int& xf, int& yf,move *& answer);
	void get_pos_from_command(int& x, int& y);
	void print_single_move(move* v)const;

	void find_y_jumped(int& yj, int xs, int ys, int yf);
	int hashed_jump(int xs, int ys, int xj, int yj, int xe, int ye);
	int rev_hash(int i);
	
	
public:	
	
	
	command_control(char t):turn(t) {
	} 
	~command_control() {

		while (!list.empty()) {
			list.pop_front();
		}

	}
	move* move_request();
	void start_round(int score, char turn)const;
	void mid_round(move * m, char turn)const;
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