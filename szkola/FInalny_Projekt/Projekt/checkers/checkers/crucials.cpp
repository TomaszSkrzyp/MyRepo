#include "board.h"
void board::reset() {
	turn = 'w';
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 4; j++) {
			

				arr[i][j] = 'b';
			
		}
	}
	for (int i = 3; i <5 ; i++) {
		for (int j = 0; j < 4; j++) {
			arr[i][j] = 'e';
		}
	}
	for (int i = 7; i > 4; i--) {
		for (int j = 0; j < 4; j++) {
			
				arr[i][j] = 'w';
			
		}
	}
}
