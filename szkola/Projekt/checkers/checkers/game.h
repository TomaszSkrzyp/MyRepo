#pragma once
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
#include "board_moves.h"
#include "player.h"
#include <memory>
#include "alpha_beta.h"

#include <thread>
#include <chrono>   
class game {
	float score=0;
	bool types[2];
	int level[2];
	player players[2];
	int evaluate_score(const board& b);
	bool on_wall(int i, int j);
	void main_loop(bool iscomp1,bool iscomp2);
	/*pobieranie ruchow i ladowanie ich do listy */
	bool load_jump_moves(std::list<move*>& moves,/*kopia poszukiwacz skokow*/ board_jumps jump_finder, const board& new_board);
	bool load_moves(std::list<move*>& moves,/*kopia poszukiwacza ruchow*/board_moves move_finder, const board& new_board);

	;
public:
	game(bool is_comp_1, int level1, bool is_comp_2,int level2);
	void start() {
		main_loop(types[0],types[1]);
	}
	bool game_over(int player_index, int list_size);
	
};

