#pragma once
#include <memory>
#include "board_jumps.h"
#include "board_moves.h"
class alpha_beta {
	 int MaxIterDepth;
	std::unique_ptr<board> current_b;
	move* bestM;
	move* temp_bestM;
	int max_depth;
	int cur_depth;
	bool reached_end;

	board_jumps jump_finder;
	board_moves move_finder;
	/*helping methods; also found in game class */
	void print_move(move* v);

	bool on_wall(int x, int y);
	int evaluate_score(const board& b);
	bool load_jump_moves(std::list<move*>& moves,/*kopia poszukiwacz skokow*/ board_jumps& jump_finder, const board& new_board);
	bool load_moves(std::list<move*>& moves,/*kopia poszukiwacza ruchow*/board_moves& move_finder, const board& new_board);
public:
	alpha_beta(std::unique_ptr<board>& board_ptr, board_jumps& jump_finding_tool, board_moves& move_finding_tool,int max) : current_b(std::move(board_ptr)), bestM(nullptr), temp_bestM(nullptr), max_depth(0), cur_depth(0),
																													reached_end(false), jump_finder(jump_finding_tool), move_finder(move_finding_tool),MaxIterDepth(max) {
		
	}
	int algorythm(std::unique_ptr<board>& b, int depth, int alpha, int beta);
	move* get_best_move(); 
	void search(std::list<move*> m_list);

};