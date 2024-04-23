#include"moves_jumps.h"


const void move::print_jumps() {
	for (auto v : jumps) {
		std::cout << v->get_xs() << " " << v->get_ys() << " " << v->get_xf() << " " << v->get_yf() << " " << v->get_piece() << "   ";
	}

}
 bool move::has_kinging_occured(char piece_after) {
	if (piece_after == piece) {
		return false;
	}
	return true;
}





