
#include "game.h"


void game::main_loop(bool iscomp1,bool iscomp2) {
	board new_board(iscomp1, iscomp2);
	board_jumps jump_finder(new_board);board_moves move_finder(new_board);
	command_control console('w');
	std::list<move*> list;
	
	int cur_player_index = 0;
	/*later remove-> mixing i/o with function*/
	
	
	for (int i = 0; i <10; i++) {
			console.start_round(evaluate_score(new_board),new_board.get_turn());
			if (!load_jump_moves(list,jump_finder,new_board)) {
				load_moves(list, move_finder, new_board);

			}
			
			if (game_over(cur_player_index,int(list.size()))){
				console.print_table(&new_board);
				return;
			}

			
			console.print_table(&new_board);
			if(list.size()!=1){
				std::unique_ptr<board> ptr = std::make_unique<board>(new_board);
				alpha_beta algo(ptr, jump_finder, move_finder, level[cur_player_index]);
				algo.search(list);
				if (level[cur_player_index] != 0) {
					list.push_front(algo.get_best_move());
				}
			}

			std::this_thread::sleep_for(std::chrono::milliseconds(3000));
			system("cls");
			new_board.make_move((players[cur_player_index]).choose_move(list , console));

			console.mid_round(new_board.get_previous_move(), new_board.get_turn());
			console.print_table(&new_board);
			std::this_thread::sleep_for(std::chrono::milliseconds(3000));
			
			cur_player_index = (cur_player_index + 1) % 2;
			while (!list.empty()) {
				

					delete list.front();

				
				list.pop_front();


			}
			system("cls");
	}
	std::cout << "It's a draw";
	return;

	
}

game::game(bool is_comp_1, int level1, bool is_comp_2, int level2) {
	player player1('w', "generic1"); player player2('b', "generic2");
	command_control console('w');
	std::cout << "Type in first player's name\n";
	player1.set_name(console.get_string());

	std::cout << "Type in first player's name\n";
	player2.set_name(console.get_string());

	std::this_thread::sleep_for(std::chrono::milliseconds(500));
	system("cls");
	level[0] = level1; level[1] = level2;
	if (is_comp_1) {
		if (level1 > 0) {
			player1.set_type(std::make_shared<smart_computer>());
		}
		else {
			player1.set_type(std::make_shared<random_comp>());
		}
		
	}
	else {
		player1.set_type(std::make_shared<human_player>());
	}
	if (is_comp_2) {
		if (level2 > 0) {
			player2.set_type(std::make_shared<smart_computer>());
		}
		else {
			player2.set_type(std::make_shared<random_comp>());
		}
	}
	else {
		player2.set_type(std::make_shared<human_player>());
	}
	types[0] = is_comp_1; types[1] = is_comp_2;
	players[0] = player1;
	players[1] = player2;
	score = 0;
};
	

bool game::load_moves(std::list<move*> &moves, board_moves move_finder,const board& new_board ) {
	move_finder.replace_board(new_board);
	move_finder.avalilable_moves();
	move_finder.update_moves(moves);
	if (!moves.empty()) {
		/*do wyrzycenia*/
		
		return true;
	}
	return false;
}
bool game::load_jump_moves(std::list<move*>& moves,  board_jumps jump_finder, const board& new_board) {
	jump_finder.replace_board(new_board);
	jump_finder.avalilable_jumps();
	jump_finder.update_moves(moves);
	if (!moves.empty()) {
		/*do wyrzycenia*/
		
		return true;
	}
	return false;
}
int game::evaluate_score(const board& b) {
	int score = 0;
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 4; j++) {

			if (tolower(b.get_piece(i, j)) == 'w') {
				if (b.get_piece(i, j) == 'W') {
					score += 200;
				}
				score += 100;
				if (on_wall(i, j)) {
					score += 5 * (7 - i);
				}

			}
			else if (tolower(b.get_piece(i, j)) == 'b') {
				if (b.get_piece(i, j) == 'B') {
					score -= 200;
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