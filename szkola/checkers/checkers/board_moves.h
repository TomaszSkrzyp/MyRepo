#pragma once
#include"board_jumps.h"
class board_moves : public general {
	void move_legal_up(char piece, int xs, int ys, char dir);
	void move_legal_down(char piece, int xs, int ys, char dir);
	

	std::list<move*> m_list;
public:
	board_moves() = default;
	board_moves(const board & b) :general(b) {
		/*std::cout << "board moves finder created" << std::endl;*/
		
	}
	

	// Destructor
	~board_moves() {
		/*std::cout << "board moves finder destroyed" << std::endl;*/
	}

	void update_moves(std::list<move*>& list);
	void add_move(char piece, int xs, int ys, int xf, int yf);
	bool avalilable_moves();
	const void print_size() {
		std::cout << m_list.size();
	}
};
