import enum
import re
import random
from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.exceptions import InvalidMove, UnknownGameScore
from tic_tac_toe.logic.validators import validate_grid, validate_game_state

WINNING_PATTERNS=(
    "???......",
    "...???...",
    "......???",
    "?...?...?",
    "..?.?.?..",
    "?..?..?..",
    ".?..?..?.",  
    "..?..?..?",      
    

)
class Mark(enum.StrEnum):#mixed data type
    CROSS = "X"
    NOUGHT = "O"
    @property
    def other(self)-> "Mark":
        return Mark.CROSS if self is Mark.NOUGHT else Mark.NOUGHT
@dataclass(frozen=True)
class Grid:
    cells: str=" "*9
    def __post_init__(self)->None:
        validate_grid(self)
    @cached_property
    def x_count(self)-> int:
        return self.cells.count("X")
    @cached_property
    def o_count(self)-> int:
        return self.cells.count("O")
    @cached_property
    def empty_count(self)-> int:
        return self.cells.count(" ")
@dataclass(frozen=True)
class Move:
    mark:Mark
    cell_index:int
    before_state: "GameState"
    after_state: "GameState"
@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark("X")

    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.o_count==self.grid.x_count:
            return self.starting_mark
        else: 
            return self.starting_mark.other
        
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count==9
    
    @cached_property
    def game_over(self)->bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self):
        return self.winner is None and self.grid.empty_count == 0
    
    @cached_property
    def winner(self)-> Mark| None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark),self.grid.cells):
                    return mark
        return None
    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []
    
    def __post_init__(self) -> None:
        validate_game_state(self)
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves
    def make_random_move(self) -> Move | None:
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None
    def make_move_to(self, index: int) -> Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=GameState(
                Grid(
                    self.grid.cells[:index]
                    + self.current_mark
                    + self.grid.cells[index + 1:]
                ),
                self.starting_mark,
            ),
        )
    def evaluate_score(self, mark:Mark):
        if self.game_over:
            if self.tie:
                return 0
            if self.winner is mark:
                return 1
            else:
                return -1
        raise UnknownGameScore("The score is unknown")
        
