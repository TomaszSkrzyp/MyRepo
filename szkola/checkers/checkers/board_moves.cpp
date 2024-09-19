#include "board_moves.h"


void board_moves::add_move(char piece, int xs, int ys, int xf, int yf) {
	move* m = new move(piece, xs, ys, xf, yf);
	m_list.push_back(m);

}
void board_moves::move_legal_up(char piece, int xs, int ys, char dir)  {
	if (dir == 'l' and ((xs % 2 - 1)!=0 or ys != 0) ){
		if (xs % 2 == 0) {
			if (arr[xs - 1][ys] == 'e') {
				add_move(piece, xs, ys, xs - 1, ys);
			}
		}
		else {
			if (arr[xs - 1][ys - 1] == 'e') {
				add_move(piece, xs, ys, xs - 1, ys - 1);
			}
		}
	}
	else if (dir == 'r' and ((xs % 2!=0) or  (3 - ys) != 0)) {
		if (xs % 2 == 0) {
			if (arr[xs - 1][ys + 1] == 'e') {
				add_move(piece, xs, ys, xs - 1, ys + 1);
			}
		}
		else {
			if (arr[xs - 1][ys] == 'e') {
				add_move(piece, xs, ys, xs - 1, ys);
			}
		}
	}
}
void board_moves::move_legal_down(char piece, int xs, int ys, char dir) {
	if (dir == 'l' and ((xs % 2 - 1) != 0 or ys != 0)) {
		if (xs % 2 == 0) {
			if (arr[xs + 1][ys] == 'e') {
				add_move(piece, xs, ys, xs + 1, ys);
			}
		}
		else {
			if (arr[xs + 1][ys - 1] == 'e') {
				add_move(piece, xs, ys, xs + 1, ys - 1);
			}
		}
	}
	else if (dir == 'r' and ((xs % 2 != 0) or (3 - ys) != 0)) {
		if (xs % 2 == 0) {
			if (arr[xs + 1][ys + 1] == 'e') {
				add_move(piece, xs, ys, xs + 1, ys + 1);
			}
		}
		else {
			if (arr[xs + 1][ys] == 'e') {
				add_move(piece, xs, ys, xs + 1, ys);
			}
		}
	}
}
bool board_moves::avalilable_moves() {
	while (!m_list.empty()) {
		m_list.pop_front();
	}
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 4; j++) {
			if (turn == 'w') {

				/*char l do poruszania w lewo i r do poruszania w prawo*/
				if (tolower(arr[i][j]) == 'w' and i != 0) {
					move_legal_up(arr[i][j], i, j, 'l');
					move_legal_up(arr[i][j], i, j, 'r');

				}
				if (arr[i][j] == 'W' and i!=7) {
					move_legal_down(arr[i][j], i, j, 'l');
					move_legal_down(arr[i][j], i, j, 'r');
				}
			}
			else {
				if (tolower(arr[i][j]) == 'b' and i != 7) {
					move_legal_down(arr[i][j], i, j, 'l');
					move_legal_down(arr[i][j], i, j, 'r');

				}
				if (arr[i][j] == 'B' and i!=0) {
					move_legal_up(arr[i][j], i, j, 'l');
					move_legal_up(arr[i][j], i, j, 'r');
				}

			}
		}
	}
	
	
	
	if (m_list.size()!=0) {
		return true;
	}
	return false;
}
void board_moves::update_moves(std::list<move*>& list)  {
	while (!list.empty()) {
		list.pop_front();
	}
	for (auto v : m_list) {
		list.push_back(v);
	}
}
		