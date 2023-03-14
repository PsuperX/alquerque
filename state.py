from board import Action, Board, List
from dataclasses import dataclass, field


@dataclass()
class State:
    board: Board
    history: List[Action] = field(default_factory=list)
    cur_hist: int = 0

    def execute(self, action: Action):
        del self.history[self.cur_hist :]
        self.history.append(action)
        self.cur_hist += 1
        action.execute()

    def undo(self):
        self.cur_hist -= 1
        self.history[self.cur_hist].undo()
        pass

    def redo(self):
        pass
