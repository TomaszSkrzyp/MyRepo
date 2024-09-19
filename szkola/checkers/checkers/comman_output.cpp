#include "command.h"
//command printing things at the start of the game
void command_control::start_game() const {
	std::cout << "Player named " << players[0] << " gets color ";
	if (turn == 'w') {
		std::cout << "white.\nPlayer named " << players[1] << " gets color black.\n";
	}
	else if (turn == 'b') {
		std::cout << "black.\nPlayer named " << players[1]<< " gets color white.\n";

	}

	std::this_thread::sleep_for(std::chrono::milliseconds(5000));
	system("cls");

}

//command printing things at the start of each round
void command_control::start_round(int score, char turn) const{
	std::cout << " It is ";
	if (turn == 'w') {
		std::cout <<players[0]<<"'s turn. Color: white";
	}
	else {
		std::cout << players[1]<<"'s turn. Color: black";
	}
	std::cout << "\nCurrent score: " << score;
}
//command informing about a made move
void command_control::mid_round(move *m, char turn) const{

	system("cls");
	if (turn == 'b') {
		std::cout << players[0];
	}
	else {
		std::cout << players[1];
	}
	std::cout << " has made a move:\n";
	print_single_move(m);

}
//command informing about how this move changed score
void command_control::move_strength(int cur_score, int score_after) const {
	if (turn == 'w') {
		std::cout << "\nThis move value for white is: " << score_after - cur_score;
	}
	else if (turn == 'b') {
		std::cout << "\nThis move value black is: " << -score_after + cur_score;

	}

	std::this_thread::sleep_for(std::chrono::milliseconds(3000));
	system("cls");

}
//function clearing lines
void command_control::clear_lines(int n_lines)const {
	std::cout << "\r";
	std::cout << "\033[2K";
	for (int i = 0; i < n_lines; i++) {
		std::cout << "\033[1A";
		std::cout << "\033[2K";
	}

}


//prints move in a string format
void command_control::print_single_move(move* v) const{

	/*operation on y to convert programs column number to real column nbumber*/
	/*operation on x to convert prgrams row number to letter format*/
	std::cout << char(2 * v->get_ys() + (v->get_xs() + 1) % 2 + 65) << ", " << v->get_xs() + 1 << " -> " << char(2 * v->get_yf() + (v->get_xf() + 1) % 2 + 65) << ", " << v->get_xf() + 1;
	if (!v->jumps.empty()) {
		std::cout << " consisting of: ";
	}
	for (auto j : v->jumps) {
		std::cout << char(2 * j->get_ys() + (j->get_xs() + 1) % 2 + 65) << ", " << j->get_xs() + 1 << " -> " << char(2 * j->get_yf() + (j->get_xf() + 1) % 2 + 65) << ", " << j->get_xf() + 1 << "    ";

	}

}
//prints move in a string format
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
// print avalilable moves
void command_control::print_move() const {
	int i = 1;

	printf("\033[%d;%dH", i, 50);
	std::cout << "Current avalilable moves";
	i += 1;
	for (auto v : list) {

		printf("\033[%d;%dH", i, 50);
		std::cout <<v->jumps.size() << "   ";
		print_single_move(v);
		i += 1;
		
	}

	printf("\033[%d;%dH", 22, 0);
}
//command informing about game finish
bool command_control::end_game(bool is_draw, int index) {
	if (is_draw) {
		std::cout << "\nIt is a draw!";
	}
	else {
		std::cout << "\nPlayer " << players[index] << " has won!!";
	}
	std::cout << " Do you want to play once again?\n Press \"y\" if so. Otherwise press anything but \"y\" ";
	char l;
	std::cin >> l;
	if (l == 'y') {
		return true;
	}
	else {
		return false;
	}
	system("cls");
}
