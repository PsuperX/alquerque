from board import Board
from state import State
from game import (
    Game,
    execute_minimax_move,
    execute_player_move,
    execute_random_move,
    execute_negamax_move,
    execute_minimax_move_with_transposition,
)
from gui import Renderer, jogo
from eval_fncs import eval_1


def main_menu_phase(renderer: Renderer | None):
    """
    Main menu loop
    """
    if renderer:
        renderer.intro_screen()


def gameplay_phase(num_rows, num_cols, renderer: Renderer | None = None):
    """
    Gameplay loop
    """
    s = State(Board(num_rows, num_cols))
    escolh_game = {
        1: lambda x, y: execute_random_move,
        2: execute_minimax_move,
        3: lambda x, y: execute_player_move,
        4: execute_negamax_move,
        5: execute_minimax_move_with_transposition,
    }

    game = Game(
        s,
        escolh_game[jogo[0][0]](eval_1, jogo[0][1]),
        escolh_game[jogo[1][0]](eval_1, jogo[1][1]),
        renderer,
    )

    game.start()


def main():
    num_rows = 5
    num_cols = 5
    renderer = Renderer(num_rows, num_cols)
    # renderer = None

    while True:
        main_menu_phase(renderer)
        gameplay_phase(num_rows, num_cols, renderer)


if __name__ == "__main__":
    main()
