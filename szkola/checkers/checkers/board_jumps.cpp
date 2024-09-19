#include "board_jumps.h"


bool board_jumps::create_jump(std::list<jump*> j_list, char piece, int xs, int ys,int xj,int yj, int xf, int yf, jump* prev) {
	
	int key = hashed_jump(xs,ys, xj,yj, xf, yf);
	/*obiekttypu skok sluzacy do sprawdzenia czy w liscie nie wystapil juz ten skok lub skok odwrotny */
	jump* check = prev;

	while (check != nullptr) {
		
		if (key == prev->get_key() || rev_hash(key) == prev->get_key()) {
			std::cout << "same move" << std::endl;
			return false;
		}
		check =check->get_prev();

	}	


	jump* j = new jump(piece, arr[xj][yj], xj, yj, xs, ys, xf, yf, prev, key);
	/*std::cout << "  new jump created  " << "\n" << j << "\n";*/
	if (prev != nullptr) {
		prev->set_next(true);
	}
	j_list.push_front(j);
	avalilable_jump(xf,yf,j,j_list);
	return true;

}
/*converts a list of jumps innto a move and ads it to board's m_list*/
void board_jumps::create_jump_move(std::list<jump*> j_list) {
	if (j_list.size() != 0) {
		std::list<jump*>::const_iterator it= j_list.begin();
		for (; it != j_list.end(); it++) {

			if (!(*it)->get_next()){

				move* m = new move((*it)->get_piece(), -1, -1, -1, -1);
				
				jump* jp = *it;
				while (jp != nullptr) {
					m->jumps.push_front(jp);
					++jp->n_jump;
					jp = jp->get_prev();
					/*first->last*/
				}

				m->set_start(m->jumps.front()->get_xs(), m->jumps.front()->get_ys());
				m->set_finish(m->jumps.back()->get_xf(), m->jumps.back()->get_yf());
				

				m_list.push_front(m);
			}

		}


	}
}
void board_jumps::avalilable_jump(int xs,int ys,jump* prev,std::list<jump*>& j_list) {
			if (ys != 0) {
				if (tolower(turn) == 'w' or turn == 'B') {

					check_jump(turn, xs, ys, 'l', 'u', prev, j_list);
				}
				/*u-bicie w gore,d-bicie w dol*/
				if (tolower(turn) == 'b' or turn == 'W') {
					check_jump(turn, xs, ys, 'l', 'd', prev, j_list);
				}
			}
			if (ys != 3) {
				if (tolower(turn) == 'w' or turn == 'B') {

					check_jump(turn, xs, ys, 'r', 'u', prev, j_list);
				}
				/*u-bicie w gore,d-bicie w dol*/
				if (tolower(turn) == 'b' or turn == 'W') {
					check_jump(turn, xs, ys, 'r', 'd', prev, j_list);
				}

			}
}

void board_jumps::check_jump(char jumping_piece, int xs, int ys, char direction_y, char direction_x,jump* prev,std::list<jump*> j_list) {
	int x_jumped; int y_jumped;
	int x_finish; int y_finish;
	char required_jumped_piece;
	char jumped_piece;
	/*ustalanie wspolrzednej pionowej polozenia poinka w ruchu*/
	if (direction_x == 'u') {
		if (xs < 2) {
			if (j_list.size() != 0) {
				if (m_list.size() == 0 or m_list.front()->jumps.back()->get_key() != j_list.front()->get_key()) {
					/*std::cout << j_list.size() << " creating: " << prev->get_xs() << " " << prev->get_ys() << " " << prev->get_xf() << " " << prev->get_yf() << " " << " " << jumping_piece << std::endl;*/
					create_jump_move(j_list);
				}
			}

			return;
		}
		x_finish = xs - 2; x_jumped = xs - 1;
	}
	else {  
		if (xs > 5) {
			if (j_list.size() != 0) {
				if (m_list.size() == 0 or m_list.front()->jumps.back()->get_key() != j_list.front()->get_key()) {
					/**std::cout << j_list.size() << " creating: " << prev->get_xs() << " " << prev->get_ys() << " " << prev->get_xf() << " " << prev->get_yf() << " " << " " << jumping_piece << std::endl;*/
					create_jump_move(j_list);
				}
			}
			return;
		}
		x_finish = xs + 2; x_jumped = xs + 1;	
	}
	/*ustalanie wspolrzednej poziomej polozenia poinka w ruchu*/
	if (direction_y == 'l') {
		y_finish = ys - 1;
	}
	else{
		y_finish = ys + 1;
	}
	find_y_jumped(y_jumped, xs, ys, y_finish);
	/*ustalanie przeskakiwanego piona i wymaganego przeskakiwanego piona*/
	jumped_piece = arr[x_jumped][y_jumped];
	if (tolower(jumping_piece) == 'b') {
		required_jumped_piece = 'w';
	}
	else {
		required_jumped_piece = 'b';
	}
	
	/*wlasciwa czesc funkcji*/
	if (arr[x_finish][y_finish] == 'e' and tolower(jumped_piece) == required_jumped_piece) {
		
		
		if (!create_jump(j_list, turn, xs, ys, x_jumped, y_jumped, x_finish, y_finish, prev)) {
			
			/*std::cout << "not adding move " << xs << " " << ys << " " << x_jumped << " " << y_jumped << " " << x_finish << " " << y_finish << " " << jumped_piece << " " << jumping_piece << " " << direction_x << direction_y << std::endl; */
			return;

		}
		/*std::cout << "adding move " << xs << " " << ys << " " << x_jumped << " " << y_jumped << " " << x_finish << " " << y_finish << " " << jumped_piece << " " << jumping_piece << " " << direction_x << direction_y << std::endl; */
		
		
	}
	else {
		if (j_list.size()!=0){
			if (m_list.size() == 0 or m_list.front()->jumps.back()->get_key() != j_list.front()->get_key()) {
				/*std::cout << j_list.size() << " creating: " << prev->get_xs() << " " << prev->get_ys() << " " << prev->get_xf() << " " << prev->get_yf() << " " << jumped_piece << " " << jumping_piece << std::endl; */
				create_jump_move(j_list);
			}
		}
	}
	
}

bool board_jumps::avalilable_jumps() {
	while (!m_list.empty()) {
		m_list.pop_front();
	}

	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 4; j++) {
			if (tolower(arr[i][j]) == turn) {
				std::list<jump*> j_list = {};
				avalilable_jump(i, j, nullptr, j_list);
			}
		}

	}
	if (m_list.size() == 0) {
		return false;
	}
	return true;
}
void board_jumps::update_moves(std::list<move*>& list)  {
	while (!list.empty()) {
		list.pop_front();
	}
	for (auto v : m_list) {
		list.push_front(v);
	}
}


	

	
				





		


	




