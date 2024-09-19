#include "board.h"
#include "board_jumps.h"
#include <stdlib.h>
#include <crtdbg.h>
#include "game.h"
#include <iostream>
int main() {
	 game this_game(false,6,true,6);
	 this_game.start();
	

	return 0;
}