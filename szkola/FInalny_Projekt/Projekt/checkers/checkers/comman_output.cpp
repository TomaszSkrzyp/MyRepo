#include "command.h"
void command_control::start_round(int score, char turn) const{
	std::cout << " It is ";
	if (turn == 'w') {
		std::cout << "white's turn";
	}
	else {
		std::cout << "black's turn";
	}
	std::cout << "\nCurrent score: " << score;
}
void command_control::mid_round(move *m, char turn) const{
	
	if (turn == 'w') {
		std::cout << "White";
	}
	else {
		std::cout << "Black";
	}
	std::cout << " has made a move:\n";
	print_single_move(m);
	

}
void command_control::print_single_move(move* v) const{
	std::cout << char(2 * v->get_ys() + (v->get_xs() + 1) % 2 + 65) << ", " << v->get_xs() + 1 << " -> " << char(2 * v->get_yf() + (v->get_xf() + 1) % 2 + 65) << ", " << v->get_xf() + 1;
	if (!v->jumps.empty()) {
		std::cout << " consisting of: ";
	}
	for (auto j : v->jumps) {
		std::cout << char(2 * j->get_ys() + (j->get_xs() + 1) % 2 + 65) << ", " << j->get_xs() + 1 << " -> " << char(2 * j->get_yf() + (j->get_xf() + 1) % 2 + 65) << ", " << j->get_xf() + 1 << "    ";

	}
	std::cout << "\n";

}
void command_control::this_move_command(move* m) const {
	std::cout << m->get_xs() << ", " << m->get_ys() << " -> " << m->get_xf() << ", " << m->get_yf() << "\n";
	std::cout << "\n";
}
void command_control::print_table(const board* b) const {
	std::cout << "\n"<<"   ";
	for (int i = 65; i < 73; i++) {
		std::cout << char(i)<<"   ";
	}
	for (int i = 0; i < 8; i++) {
		std::cout << "\n" << "----------------------------------" << "\n";
		std::cout << i+1<<"| ";
		if (i % 2 == 0) {
			std::cout << "  ";
		}
		for (int j = 0; j < 4; j++) {
			if (i % 2 == 0) {
				std::cout <<"| "<<char(b->get_piece(i, j)) << " |   ";

			}
			else {
				std::cout << char(b->get_piece(i, j)) << " |   | ";
			}
		}
	}

	std::cout << "\n" << "----------------------------------" << "\n";
}
void command_control::print_move() const {

	for (auto v : list) {
		std::cout << "     \n   " << v->jumps.size() << "         ";
		/*operation on y to convert programs column number to real column nbumber*/
		/*operation on x to convert prgrams row number to letter format*/
		print_single_move(v);
	}
}