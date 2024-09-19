#include"board.h"
void board::reset() {
	turn = 'w';
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 4; j++) {


			arr[i][j] = 'b';

		}
	}
	for (int i = 3; i <5; i++) {
		for (int j = 0; j < 4; j++) {
			arr[i][j] = 'e';
		}
	}
	for (int i = 7; i > 4; i--) {
		for (int j = 0; j < 4; j++) {

			arr[i][j] = 'w';

		}
	}


}
board::board(char w_is_computer,char b_is_computer) {
	is_computer[0] = w_is_computer;is_computer[1] = b_is_computer;
	/*std::cout << "board created" << std::endl;*/
	reset();
}
board::board(const board& board) :turn(board.turn) {
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 8; j++) {
			arr[i][j] = board.arr[i][j];

		}
	}
	is_computer[0] = board.is_computer[0];
	is_computer[1] = board.is_computer[1];

}
board::~board() {
	while (!previous_moves.empty()) {
		delete previous_moves.front();
		previous_moves.pop_front();
		
	}
	/*std::cout << "board destroyed" << std::endl;*/
}
char board::get_piece(int x, int y) const {
	return arr[x][y];
}
void board::make_move(move* chosen_move) {
	int start[2] = {chosen_move->get_xs(),chosen_move->get_ys()};
	int finish[2] = {chosen_move->get_xf(),chosen_move->get_yf()};
	for (auto v : chosen_move->jumps) {
		arr[v->get_xj()][v->get_yj()] = 'e';
	}
	char piece = arr[start[0]][start[1]];
	arr[start[0]][start[1]] = 'e';
	arr[finish[0]][finish[1]] = piece;
	change_turn();
	move* prev_move = new move(*chosen_move);

	/*std::cout << "  new prev_move created  " << "\n" << prev_move << "\n";*/
	previous_moves.push_back(prev_move);
	check_crown(finish[0], finish[1]);
	
}

void board::undo_move() {
	 int start[2] = { get_previous_move()->get_xs(),get_previous_move()->get_ys()};
	int finish[2] = {get_previous_move()->get_xf(),get_previous_move()->get_yf()};
	for (auto v : get_previous_move()->jumps) {
		arr[v->get_xj()][v->get_yj()] = v->get_jumped_piece();
	}
	char piece = arr[finish[0]][finish[1]];
	arr[start[0]][start[1]] = piece;
	arr[finish[0]][finish[1]] = 'e';
	change_turn();
		arr[start[0]][start[1]] = tolower(piece);
	

	delete get_previous_move();
	previous_moves.pop_back();
}
void board::check_crown(const int& x, const int& y) {
	if (x == 7 and arr[x][y] == 'b') {
		arr[x][y] = 'B';
	}
	if (x == 0 and arr[x][y] == 'w') {
		arr[x][y] = 'W';
	}
	
}

move* board::get_previous_move() const {
	return previous_moves.back();
}

void board::change_turn() {
	if (turn == 'w') {
		turn = 'b';

	}
	else {
		turn = 'w';
	}
}
 char board::get_turn() const {
	return turn;
}
 bool board::is_player_computer(int ind) const {
	 return is_computer[ind];
}

