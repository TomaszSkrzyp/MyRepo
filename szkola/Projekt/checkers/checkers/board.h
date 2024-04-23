#pragma once
#include <iostream>
#include <list>
#include"moves_jumps.h"
class board {
	char arr[8][4];
	char turn;
	bool is_computer[2];
	std::list<move*> previous_moves;
	void check_crown(const int& x, const int& y);

	void reset();


public:
	char get_piece(int x, int y) const;
	board(char w_is_computer, char b_is_computer);
	~board();
	board(const board& board);
	move* get_previous_move()const;
	
	void make_move(move* chosen_move);
	void undo_move();
	void change_turn();
	char get_turn() const;
	bool is_player_computer(int ind) const;

};