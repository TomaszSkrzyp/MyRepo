#include"game.h"

bool game::game_over(int player_index,int list_size) {
	if (list_size==0) {
		std::cout << "Player " << players[player_index].get_name() << " has no more moves\n";

		std::cout << "Player " << players[(player_index+1)%2].get_name() << " wins\n";
		return 1;

	}
	return 0;
}
bool game::on_wall(int x, int y) {
	if ((x % 2) == 1 and y == 0) {
		return true;
	}
	else {
		if ((x % 2) == 0 and y == 3) {
			return true;
		}
	}
	return false;
}
