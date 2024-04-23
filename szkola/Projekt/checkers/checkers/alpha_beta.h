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
	/*helping methods; also found in game cpp*/
	bool on_wall(int x, int y);
	int evaluate_score(const board& b);
	bool load_jump_moves(std::list<move*>& moves,/*kopia poszukiwacz skokow*/ board_jumps& jump_finder, const board& new_board);
	bool load_moves(std::list<move*>& moves,/*kopia poszukiwacza ruchow*/board_moves& move_finder, const board& new_board);
public:
	alpha_beta(std::unique_ptr<board>& board_ptr, board_jumps& jump_finding_tool, board_moves& move_finding_tool,int max) : current_b(std::move(board_ptr)), bestM(nullptr), temp_bestM(nullptr), max_depth(0), cur_depth(0),
																													reached_end(false), jump_finder(jump_finding_tool), move_finder(move_finding_tool),MaxIterDepth(max) {
		
	}
	int algorythm(std::unique_ptr<board>& b, int depth, int alpha, int beta) {
		/*if (depth == 0) {
			std::cout << "\n"<<depth;
			reached_end = true;
			cur_depth = max_depth;
			if (b->get_turn() == 'b') {
				return std::numeric_limits<int>::max();
			}
			else {
				return std::numeric_limits<int>::min();
			}
		}*/
		reached_end = false;
		if (depth == 0) {

			return evaluate_score(*b);
		}
		
		std::list<move*> m_list;
		if (!load_jump_moves(m_list, jump_finder, *current_b)) {
			load_moves(m_list, move_finder, *current_b);

		}
		std::list<move*>::iterator it = (m_list).begin();
		int localalpha = -100000000;
		int localbeta = 100000000;
		if (b->get_turn() == 'w') {
			for (; it != (m_list).end(); ++it) {



				(*b).make_move(*it);
				std::unique_ptr<board> new_board(new board(*b));
				int value = algorythm(new_board, depth - 1,alpha, std::min(localbeta,beta));
				/*std::cout << "\n" << value << " value of move: ";
				print_move(*it);
				std::cout << "\n";*/
				(*b).undo_move();
				if (value >alpha) {
					alpha = value;
					if (depth == max_depth) {
						if (temp_bestM != nullptr) {
							delete temp_bestM;
						}

						temp_bestM = new move(*(*it));

					}
				}

				/*wycina mozliwosci ktore wiadomo ze nie bede lepsze od najlepszego dotychczas*/
				if (alpha >= beta and depth<max_depth) {
					while (!m_list.empty()) {
						delete m_list.front();
						m_list.pop_front();

					}
					return alpha;
				}

			}
			while (!m_list.empty()) {
				delete m_list.front();
				m_list.pop_front();

			}
			if (depth == max_depth) {
				cur_depth = depth;
			}

			return alpha;


		}
		else if (b->get_turn() == 'b') {
			for (; it != (m_list).end(); ++it) {

				

				(*b).make_move(*it);
				std::unique_ptr<board> new_board(new board(*b));
				int value = algorythm(new_board, depth - 1, std::max(localalpha, alpha), beta);
				/*std::cout << "\n" << value << " value of move: ";
				print_move(*it);
				std::cout << "\n";*/
				(*b).undo_move();
				if (value < beta) {
					beta = value;
					if (depth == max_depth) {
						if (temp_bestM != nullptr) {
							delete temp_bestM;
						}
						
						temp_bestM = new move(*(*it));

					}
				}
				
				/*wycina mozliwosci ktore wiadomo ze nie bede lepsze od najlepszego dotychczas*/
				if (alpha >= beta) {
					while (!m_list.empty()) {
						delete m_list.front();
						m_list.pop_front();

					}
					return beta;
				}

			}
			while (!m_list.empty()) {
				delete m_list.front();
				m_list.pop_front();

			}
			if (depth == max_depth) {
				cur_depth = depth;
			}
			
			return beta;


		}


	}
	move* get_best_move() {
		std::cout << "\nBEST MOVE IN POSI: ";
		print_move(bestM);
		std::cout << "n";
		return bestM;
	}
	void search(std::list<move*> m_list) {
		if (MaxIterDepth == 0) {
			return;
		}
		
		for (int i = 1; i <= MaxIterDepth; i++) {
				max_depth = i;
				
				algorythm(current_b, i, std::numeric_limits<int>::min(), std::numeric_limits<int>::max());

				
				bestM = temp_bestM;
				if (reached_end) {
					std::cout << "ending";
					break;
				}
		}
		if (bestM == nullptr) {
				return;
		}
			
		
	}

	void print_move(move* v) {
		std::cout << char(2 * v->get_ys() + (v->get_xs() + 1) % 2 + 65) << ", " << v->get_xs() + 1 << " -> " << char(2 * v->get_yf() + (v->get_xf() + 1) % 2 + 65) << ", " << v->get_xf() + 1;
		if (!v->jumps.empty()) {
			std::cout << " consisting of: ";
		}
		for (auto j : v->jumps) {
			std::cout << char(2 * j->get_ys() + (j->get_xs() + 1) % 2 + 65) << ", " << j->get_xs() + 1 << " -> " << char(2 * j->get_yf() + (j->get_xf() + 1) % 2 + 65) << ", " << j->get_xf() + 1 << "    ";

		}
		std::cout << "\n";
	}
};