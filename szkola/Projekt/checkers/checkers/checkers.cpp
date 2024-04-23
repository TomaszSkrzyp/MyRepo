#include "board.h"
#include "board_jumps.h"
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
#include "game.h"
#include <iostream>
int main() {
	 game this_game(true,0,true,0);
	 this_game.start();

	_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_DEBUG);
	_CrtDumpMemoryLeaks();
	

	return 0;
}