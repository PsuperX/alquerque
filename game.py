from dataclasses import dataclass
import random
from state import State

@dataclass
class Game:

    def start(self, log_mov = False):
        self.state = State()
        result = -1
        while True:
            if self.state.board.next_player == 1:
                self.player1_AI(self)
            else:
                self.player2_AI(self)

            if log_mov:
                print(self.state.board)

            result = self.state.board.is_terminal()
            if result != 0:
                break

        if result == 3:
            print("Nobothy wins :/")
        else:
            print(f"Player {result} Wins :D")

##############################################################################

def execute_random_move(game: Game):
    move = random.choice(game.state.board.get_valid_actions())
    game.state.execute(move)




