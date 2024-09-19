#pragma once
#include"general.h"
class board_jumps:public general{
private:
	/**
 * ... text ...
 */
		bool create_jump(std::list<jump*> j_list, char p, int xs, int ys, int xj, int yj, int xf, int yf, jump* prev_jump);
	/*sklejenie obiektu move z obiektow typu jump*/
		void create_jump_move(std::list<jump*> j_list);

		void check_jump(char jumping_piece, int xs, int ys, char direction_y, char direction_x, jump* prev, std::list<jump*> j_list);
		

public:

	
	board_jumps(const board& b): general(b){
		/*std::cout << "board jumps finder created" << std::endl;*/
	}
	~board_jumps() {
		/*std::cout << "board jumps finder destructed" << std::endl;*/
	}

	/**
 * ... text ...
 */
	void update_moves(std::list<move*>& list);/**
 * ... text ...
 */
	void avalilable_jump(int xs, int ys, jump* prev, std::list<jump*>& j_list);
	bool avalilable_jumps();
	char get_turn()const {
		/**
 * ... text ...
 */
		return turn;
	}
	void print_size() const {
		std::cout << m_list.size();
	}
};
