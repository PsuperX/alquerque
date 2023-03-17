from typing import List, Protocol, Tuple
from dataclasses import dataclass


class Action(Protocol):
    def execute(self):
        ...

    def undo(self):
        ...


@dataclass
class Board:
    num_rows: int
    num_cols: int
    grid: List[int]
    next_player: int

    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        next_player: int,
        grid: List[int] = [],
    ) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.next_player = next_player
        if len(grid) != 0:
            self.grid = grid
        else:
            self.grid = initial_board(num_rows, num_cols)

    def is_valid_pos(self, x: int, y: int) -> bool:
        return 0 <= x < self.num_cols and 0 <= y < self.num_rows

    def get_piece(self, x: int, y: int) -> int:
        if self.is_valid_pos(x, y):
            return self.grid[(y * self.num_rows) + x]
        raise IndexError(f"No such piece x:{x} y:{y}")

    def set_piece(self, x: int, y: int, val: int) -> None:
        if not self.is_valid_pos(x, y):
            raise IndexError(f"No such piece x:{x} y:{y}")
        self.grid[(y * self.num_rows) + x] = val

    def _get_actions_inner(
        self, x: int, y: int, dirs: List[Tuple[int, int]]
    ) -> List[Action]:
        ret = []
        for dir in dirs:
            x2 = x + dir[0]
            y2 = y + dir[1]
            if (
                not self.is_valid_pos(x2, y2)
                or self.get_piece(x2, y2) == self.next_player
            ):
                continue
            elif self.get_piece(x2, y2) == 0:
                ret.append(Move((x, y), (x2, y2), self))
            elif (
                self.is_valid_pos(dx := x + 2 * dir[0], dy := y + 2 * dir[1])
                and self.get_piece(dx, dy) == 0
            ):
                ret.append(Eat((x, y), (x2, y2), (dx, dy), self))

        eats = list(filter(lambda x: isinstance(x, Eat), ret))
        if len(eats) != 0:
            return eats
        return ret

    def even_actions(self, x: int, y: int) -> List[Action]:
        """
        Ações para casas pares
        Impares + Diagonais
        """

        dirs = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        odd = self.odd_actions(x, y)
        return odd + self._get_actions_inner(x, y, dirs)

    def odd_actions(self, x: int, y: int) -> List[Action]:
        """
        Ações para casas pares
        Cima baixo esquerda ou direita
        """
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        return self._get_actions_inner(x, y, dirs)

    def get_piece_actions(self,x,y):

        if (x + y) % 2 == 0:
            return self.even_actions(x, y)
        else:
            return self.odd_actions(x, y)


    def get_valid_actions(self) -> List[Action]:
        """
        Get all actions for the current player
        """
        ret = []
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                if self.get_piece(x, y) != self.next_player:
                    continue

                if (x + y) % 2 == 0:
                    ret += self.even_actions(x, y)
                else:
                    ret += self.odd_actions(x, y)

        eats = list(filter(lambda x: isinstance(x, Eat), ret))
        if len(eats) != 0:
            return eats
        return ret

    def is_terminal(self):
        """
        Perguntar ao prof!!!
        ver se o jogo acabou
        """

        #0-continue, 1- P1 win 2- P2 win 3- Draw
        c1 = c2 = 0

        for v in self.grid:
            if v == 1:
                c1 += 1
            elif v == 2:
                c2 += 1


        if c1 == 0:
            return 2
        elif c2 == 0:
            return 1
        elif c1 == c2 == 1 and len(list(filter(lambda x: isinstance(x, Eat), self.get_valid_actions()))) == 0:
            return 3

        return 0




@dataclass
class Move:
    source: Tuple[int, int]
    dest: Tuple[int, int]
    board: Board
    change_player: bool = True

    def execute(self):
        t = self.board.get_piece(self.source[0], self.source[1])
        self.board.set_piece(self.source[0], self.source[1], 0)
        self.board.set_piece(self.dest[0], self.dest[1], t)

        if self.change_player:
            self.board.next_player = 3 - self.board.next_player

    def undo(self):
        t = self.board.get_piece(self.dest[0], self.dest[1])
        self.board.set_piece(self.dest[0], self.dest[1], 0)
        self.board.set_piece(self.source[0], self.source[1], t)

        if self.change_player:
            self.board.next_player = 3 - self.board.next_player


@dataclass
class Eat:
    hunter: Tuple[int, int]
    target: Tuple[int, int]
    dest: Tuple[int, int]
    board: Board

    def execute(self):
        Move(self.hunter, self.dest, self.board).execute()
        self.board.set_piece(self.target[0], self.target[1], 0)


    def undo(self):
        t = 3 - self.board.get_piece(self.dest[0], self.dest[1])
        Move(self.hunter, self.dest, self.board).undo()
        self.board.set_piece(self.target[0], self.target[1], t)


def initial_board(num_rows: int, num_cols: int) -> List[int]:
    # fmt: off
    return [1,1,1,1,1,
            1,1,1,1,1,
            1,1,0,2,2,
            2,2,2,2,2,
            2,2,2,2,2]
    # fmt: on
