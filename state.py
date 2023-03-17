from board import Action, Board, List, Eat
from dataclasses import dataclass, field


@dataclass
class StateController:
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

@dataclass
class State:
    controller: StateController
    board: Board

    def execute(self, action: Action):
        self.controller.execute(action)

        if isinstance(action, Eat):
            if not self.killing_streak(action):
                self.board.next_player = 3 - self.board.next_player


    def killing_streak(self,action):
        """ caso peça jogada ainda poder comer
        o jogador continua a jogar com esse mesmo objeto"""

        return len(list(filter(lambda x: isinstance(x, Eat), self.board.get_piece_actions(action.dest[0],action.dest[1])))) > 0






