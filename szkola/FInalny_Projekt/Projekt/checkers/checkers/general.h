#pragma once
#include <vector>
#include<iostream>
#include <String>
#include<cmath>
#include<list>
#include"board.h"

class general {
protected:
	char turn;
	const void find_y_jumped(int& yj, int xs, int ys, int yf);
	const int hashed_jump(int xs, int ys, int xj, int yj, int xe, int ye);
	const int rev_hash(int i);
	char arr[8][4];


public:
	virtual void update_moves(std::list<move*>& list) = 0;
	general(const board& b):turn( b.get_turn()){
		/*std::cout << "general created" << std::endl;;*/
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				arr[i][j] = b.get_piece(i,j);

			}
		}
	}
	
	~general();
	std::list<move*> m_list = {};

	
/*jumps*/
	void replace_board(const board &b);
	int get_turn() const{
		return turn;
	}
	int set_turn( char t) {
		turn = t;
	}



};

