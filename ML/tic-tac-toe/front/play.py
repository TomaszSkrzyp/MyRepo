from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.game.players import RandomComputerPlayer
from tic_tac_toe.logic.models import Mark
from console.players import ConsolePlayer
from console.renderers import ConsoleRenderer

player1,player2 = ConsolePlayer(Mark("X")), RandomComputerPlayer(Mark("O")),


TicTacToe(player1, player2, ConsoleRenderer()).play()