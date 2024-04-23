#include"command.h"
std::string command_control::get_string() const{
	std::string str;
	
	std::cin >> str;
	return str;


}
void command_control::replace_moves(const std::list<move*>& new_list, char t) {
	turn = t;
	while (!list.empty()) {
		list.pop_front();
	}
	for (auto v : new_list) {
		list.push_back(v);

	}

}
bool command_control::one_move_request(std::list<int>& keys, int& xs, int& ys, int& xj, int& yj, int& xf, int& yf,move*& answer) {
	std::cout << "Now type in finishing position\n";
	get_pos_from_command(xf, yf);
	if (abs(xs - xf) == 1) {
		if (keys.size() != 0 or list.front()->jumps.size() != 0) {
			std::cout << "ZA NIEBICIE TRACISZ ZYCIE\n";
			move_request();
			return false;
		}
		for (auto v : list) {
			if (v->get_xs() == xs and v->get_ys() == ys and v->get_xf() == xf and v->get_yf() == yf) {
				std::cout << "Move:" << v->get_xs() << v->get_ys() << " " << xf << yf << " is avalilable";
				answer = v;
				return true;
			}
		}
		std::cout << "nie ma takiego ruchu";
		move_request();
		return false;
	}
	xj = (xs + xf) / 2;
	find_y_jumped(yj, xs, ys, yf);
	std::cout << xj << yj;
	keys.push_back(hashed_jump(xs, ys, xj, yj, xf, yf));
}


move* command_control::move_request() {
	std::list<int> keys;
	if (turn == 'w') {
		std::cout << "It's white's turn\n";
	}
	else {
		std::cout << "It's black's turn\n";
	}
	move* answer = nullptr;
	int xs; int ys; int xf; int yf; int xj; int yj;
	get_pos_from_command(xs, ys);
	while (one_move_request(keys, xs, ys, xj, yj, xf, yf, answer) != true) {
		std::cout << " Type in \"finish\" to finish or anything else to continue\n";
		std::string buf;
		std::cin >> buf;
		if (buf == "reset") {
			return move_request();
			break;
		}
		for (auto v : list) {
			if (keys.size() == v->jumps.size()) {
				std::list<int>::iterator it; std::list<jump*>::iterator itr = v->jumps.begin();
				bool wrong_move = false;
				for (it = keys.begin(); it != keys.end(); it++) {
					std::cout << " " << *it << " " << (*itr)->get_key() << "\n";
					if (*it != (*itr)->get_key()) {
						if (buf == "finish") {
							std::cout << "This move is not avalilable" << v->get_xs() << v->get_ys() << xf << yf;
							continue;
						}
						wrong_move = true;
					}
					itr++;
				}
				if (!wrong_move) {
					std::cout << "Move:" << v->get_xs() << v->get_ys() << " " << xf << yf << " is avalilable";
					return v;
					break;

				}
			}
			
		}
		if (buf == "finish") {
			return move_request();
			break;
		}
		else {
			xs = xf; ys = yf;
		}


	}
	if (answer == nullptr) {
		std::cout << "answer_not_done";
	}
	else {
		return answer;
	}

	return move_request();
}
void command_control::get_pos_from_command(int& x, int& y) {

	std::cout << "Type in row number\n";
	char x_buf; char y_buf;
	std::cin >>y_buf;
	std::cin >> x_buf;
	x = int(x_buf-48)-1;
	y = int(char(y_buf) -65);

	std::cout << x << "  " << y;

	if( (x % 2) == 0){
		if ((y % 2) == 0) {
			std::cout << "Choose \"black\" square\n";
			get_pos_from_command(x, y);
			return;
		}
		y = (y - 1) / 2;
		
	}
	else {
		if ((y % 2) == 1) {
			std::cout << "choose \"black\" square\n";
			get_pos_from_command(x, y);
			return;
		}
		y = y / 2;

	}
	std::cout << x<<"  " << y;
	if ((x > 7 or x<0) or (y > 4 or y<0)) {
		std::cout << "Numbers has to be a digit and \n";
		get_pos_from_command(x, y);

	}
	
}

void command_control::find_y_jumped(int& y_jumped, int xs, int ys, int yf) {
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
int command_control::hashed_jump(int xs, int ys, int xj, int yj, int xf, int yf) {
	return (xf + 1) * 10 + (yf + 1) * 1 + (xj + 1) * 1000 + (yj + 1) * 100 + (xs + 1) * 100000 + (ys + 1) * 10000;
}
int command_control::rev_hash(int i) {
	int score = 0;
	score += i % 100 * 10000;
	i -= i % 100;
	score += i % 10000;
	i -= i % 10000;
	return score += i / 10000;

}


