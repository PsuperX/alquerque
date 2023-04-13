from board import Board
from state import State
from game import (
    Game,
    execute_minimax_move,
    execute_minimax_move_with_transposition,
    execute_random_move,
    execute_negamax_move,
)
from gui import Renderer
from eval_fncs import eval_1, eval_2
import itertools
import sys


num_rows = 5
num_cols = 5
s = State(Board(num_rows, num_cols))
# g = Renderer(num_rows, num_cols)
g = None

contenders = [
    (execute_random_move, "Random Player"),
    (execute_minimax_move(eval_1, 5), "Minimax (eval_1, 5)"),
    (execute_minimax_move(eval_1, 7), "Minimax (eval_1, 7)"),
    (execute_minimax_move(eval_2, 5), "Minimax (eval_2, 5)"),
    (execute_minimax_move(eval_2, 7), "Minimax (eval_2, 7)"),
    (execute_negamax_move(eval_1, 5), "Negamax (eval_1, 5)"),
    (execute_negamax_move(eval_1, 7), "Negamax (eval_1, 7)"),
    (execute_negamax_move(eval_2, 5), "Negamax (eval_2, 5)"),
    (execute_negamax_move(eval_2, 7), "Negamax (eval_2, 7)"),
    (execute_minimax_move_with_transposition(eval_1, 5), "Minimax_tt (eval_1, 5)"),
    (execute_minimax_move_with_transposition(eval_1, 7), "Minimax_tt (eval_1, 7)"),
    (execute_minimax_move_with_transposition(eval_2, 5), "Minimax_tt (eval_2, 5)"),
    (execute_minimax_move_with_transposition(eval_2, 7), "Minimax_tt (eval_2, 7)"),
]

for p1_AI, p2_AI in list(itertools.combinations_with_replacement(contenders, 2)):
    game = Game(
        s, p1_AI[0], p2_AI[0], player1_AI_name=p1_AI[1], player2_AI_name=p2_AI[1]
    )
    game.run_n_matches(10, log_moves=False)
    sys.stdout.flush()
