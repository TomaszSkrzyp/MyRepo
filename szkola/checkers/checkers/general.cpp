#include "general.h"



void general::replace_board( const board& b) {
	turn = b.get_turn();
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 8; j++) {
			arr[i][j] = b.get_piece(i, j);

		}
	}
	
}
general::~general(){
	while (!m_list.empty()) {
		m_list.pop_front();

	}
	
}

const void general::find_y_jumped(int& y_jumped, int xs, int ys, int yf) {
	if (yf < ys) {
		if (xs % 2 == 0) {
			y_jumped = ys;
		}
		else {
			y_jumped = ys - 1;
		}
	}
	else {
		if (xs % 2 == 0) {
			y_jumped = ys + 1;
		}
		else {
			y_jumped = ys;
		}

	}
}
/*hashowanie skokow*/
const int general::hashed_jump(int xs, int ys, int xj, int yj, int xf, int yf) {
	return (xf + 1) * 10 + (yf + 1) * 1 + (xj + 1) * 1000 + (yj + 1) * 100 + (xs + 1) * 100000 + (ys + 1) * 10000;
}
const int general::rev_hash(int i) {
	int score = 0;
	score += i % 100 * 10000;
	i -= i % 100;
	score += i % 10000;
	i -= i % 10000;
	return score += i / 10000;

}




