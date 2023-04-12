from typing import Dict, Tuple
from board import Action, Board, List
from dataclasses import dataclass, field


@dataclass
class State:
    """
    Holds the board state and history
    """

    board: Board
    history: List[Action] = field(default_factory=list)
    cur_hist: int = 0

    transposition_table: Dict[int, Tuple[List[Action], int]] = field(
        default_factory=dict
    )

    def execute(self, action: Action):
        """
        Executes a action and updates the history
        """
        del self.history[self.cur_hist :]
        self.history.append(action)
        self.cur_hist += 1
        action.execute()

    def undo(self) -> bool:
        """
        Undoes the last action and updates history
        Returns False if there was no previous action
        """
        if self.cur_hist == 0:
            return False

        self.cur_hist -= 1
        self.history[self.cur_hist].undo()
        return True
