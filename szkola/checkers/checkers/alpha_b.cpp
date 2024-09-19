
/*finding best move algorythm*/
#include "alpha_beta.h"
int alpha_beta::algorythm(std::unique_ptr<board>& b, int depth, int alpha, int beta) {
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
			int value = algorythm(new_board, depth - 1, alpha, std::min(localbeta, beta));
			/*std::cout << "\n" << value << " value of move: ";
			print_move(*it);
			std::cout << "\n";*/
			(*b).undo_move();
			if (value > alpha) {
				alpha = value;
				if (depth == max_depth) {
					if (temp_bestM != nullptr) {
						delete temp_bestM;
					}

					temp_bestM = new move(*(*it));

				}
			}

			/*wycina mozliwosci ktore wiadomo ze nie bede lepsze od najlepszego dotychczas*/
			if (alpha >= beta and depth < max_depth) {
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
void alpha_beta::search(std::list<move*> m_list) {
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


