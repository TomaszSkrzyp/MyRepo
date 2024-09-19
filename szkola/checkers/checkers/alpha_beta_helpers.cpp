#include "alpha_beta.h"
int alpha_beta::evaluate_score(const board& b) {
	int score = 0;
	
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 4; j++) {
			if (tolower(b.get_piece(i, j)) == 'w') {
				if (b.get_piece(i, j) == 'W') {
					score += 2*(100+10*(i));
				}
				score += 100;
				if (on_wall(i, j)) {
					score += 3 * (7 - i);
				}

			}
			else if (tolower(b.get_piece(i, j)) == 'b') {
				if (b.get_piece(i, j) == 'B') {
					score -= 2 * (100 + 10 * (7-i));
				}
				score -= 100;
				if (on_wall(i, j)) {
					score -= 5 * i;
				}



			}
		}
	}
	return score;
}

bool alpha_beta::load_moves(std::list<move*>& moves, board_moves& move_finder, const board& new_board) {
	move_finder.replace_board(new_board);
	move_finder.avalilable_moves();
	move_finder.update_moves(moves);
	if (!moves.empty()) {
		/*do wyrzycenia*/

		return true;
	}
	return false;
}
bool alpha_beta::load_jump_moves(std::list<move*>& moves, board_jumps& jump_finder, const board& new_board) {
	jump_finder.replace_board(new_board);
	jump_finder.avalilable_jumps();
	jump_finder.update_moves(moves);
	if (!moves.empty()) {
		/*do wyrzycenia*/
		return true;
	}
	return false;
}
bool alpha_beta::on_wall(int x, int y) {
	if ((x % 2) == 1 and y == 0) {
		return true;
	}
	else {
		if ((x % 2) == 0 and y == 3) {
			return true;
		}
	}
	return false;
}
move* alpha_beta::get_best_move() {
	std::cout << "\nBEST MOVE IN POSI: ";
	print_move(bestM);
	return bestM;
}
void alpha_beta::print_move(move* v) {
	std::cout << char(2 * v->get_ys() + (v->get_xs() + 1) % 2 + 65) << ", " << v->get_xs() + 1 << " -> " << char(2 * v->get_yf() + (v->get_xf() + 1) % 2 + 65) << ", " << v->get_xf() + 1;
	if (!v->jumps.empty()) {
		std::cout << " consisting of: ";
	}
	for (auto j : v->jumps) {
		std::cout << char(2 * j->get_ys() + (j->get_xs() + 1) % 2 + 65) << ", " << j->get_xs() + 1 << " -> " << char(2 * j->get_yf() + (j->get_xf() + 1) % 2 + 65) << ", " << j->get_xf() + 1 << "    ";

	}
	std::cout << "\n";
}

