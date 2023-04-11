from board import Board, initial_board
from state import State
from game import Game, execute_minimax_move, execute_player_move, execute_random_move
import random
from gui import Renderer
from eval_fncs import eval_1, eval_2


def main_menu_phase():
    """
    Main menu loop
    """
    pass


def gameplay_phase(num_rows, num_cols, renderer: Renderer | None):
    """
    Gameplay loop
    """
    s = State(Board(num_rows, num_cols))
    # TODO: custom ai
    game = Game(s, execute_minimax_move(eval_1, 5), execute_player_move, renderer)
    game.start()


def main():
    num_rows = 5
    num_cols = 5
    renderer = Renderer(num_rows, num_cols)
    # renderer = None

    while True:
        main_menu_phase()
        gameplay_phase(num_rows, num_cols, renderer)


if __name__ == "__main__":
    main()


######################################
def temp(state):
    return random.random()


# s = State(Board(5, 5))
# game = Game(s, execute_random_move, execute_random_move)
# game.run_n_matches(1000, log_moves=False)
num_rows = 5
num_cols = 5

s = State(Board(num_rows, num_cols))
print(s.board)
g = Renderer(num_rows, num_cols)
game = Game(s, execute_random_move, execute_minimax_move(eval_1, 5), renderer=g)
game.run_n_matches(3, log_moves=True)

# # fmt: off
# grid = [0,0,0,0,2,
#         0,1,1,2,0,
#         2,2,1,1,0,
#         0,2,0,0,0,
#         1,0,0,0,0,]
# # fmt: on
# b = Board(5, 5, 2, grid)
# s = State(b)
#
# print(ac := b.get_valid_actions())
#
# s.execute(ac[0])
# print(b.grid)
# s.undo()
# print(b.grid)
#
# print(initial_board(3, 3))
#
# # fmt: off
# assert [1,1,1,1,1,
#         1,1,1,1,1,
#         1,1,0,2,2,
#         2,2,2,2,2,
#         2,2,2,2,2] == initial_board(5,5)
# # fmt: on
