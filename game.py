from dataclasses import dataclass
import time
import random
from state import State
from typing import Callable
from typing_extensions import Self
from board import Board
from gui import Renderer
import pygame


@dataclass
class Game:
    state: State
    player1_AI: Callable[[Self], None]
    player2_AI: Callable[[Self], None]
    renderer: Renderer | None = None

    def start(self, log_mov=False) -> int:
        self.state = State(Board(self.state.board.num_rows, self.state.board.num_cols))

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

            if self.renderer:
                self.renderer.render(self.state)

        if result == 3:
            print("Nobothy wins :/")
        else:
            print(f"Player {result} Wins :D")

        return result

    def run_n_matches(self, n: int, max_time: int = 3600, log_moves: bool = False):
        """
        utility function to automate n matches execution
        should return the total distribution of players wins and draws
        """
        start_time = time.time()

        results = [0, 0, 0]  # [player 1 victories, player 2 victories, draws]

        while n > 0 and time.time() - start_time < max_time:
            n -= 1
            result = self.start(log_moves)
            results[result - 1] += 1

        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[0]} victories")
        print(f"  Player 2: {results[1]} victories")
        print(f"  Draws: {results[2]} ")
        print("===============================")
        # --------------------------------------------------#


def execute_random_move(game: Game):
    move = random.choice(game.state.board.get_valid_actions())
    game.state.execute(move)


def execute_minimax_move(
    evaluate_func: Callable[[State], float], depth: int
) -> Callable[[Game], None]:
    def execute_minimax_move_aux(game: Game):
        """
        updates the game state to the best possible move (uses minimax to determine it)
        """
        best_move = None
        best_eval = float("-inf")
        actions = game.state.board.get_valid_actions()
        if len(actions) == 1:
            # There isn't much to do and this can take a longggggg time
            game.state.execute(actions[0])
            return

        for move in actions:
            game.state.execute(move)
            new_state_eval = minimax(
                game.state,
                depth - 1,
                float("-inf"),
                float("+inf"),
                False,
                game.state.board.next_player,
                evaluate_func,
            )
            if new_state_eval > best_eval:
                best_move = move
                best_eval = new_state_eval
            game.state.undo()

        assert best_move, f"Board has no valid actions {game.state.board}"
        game.state.execute(best_move)

    return execute_minimax_move_aux


def minimax(
    state: State,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
    player: int,
    evaluate_func: Callable[[State], float],
) -> float:
    if depth == 0 or state.board.is_terminal() != 0:
        return evaluate_func(state)

    if maximizing:
        max_eval = float("-inf")
        for move in state.board.get_valid_actions():
            state.execute(move)
            eval = minimax(state, depth - 1, alpha, beta, False, player, evaluate_func)
            state.undo()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in state.board.get_valid_actions():
            state.execute(move)
            eval = minimax(state, depth - 1, alpha, beta, True, player, evaluate_func)
            state.undo()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def execute_player_move(game: Game):
    assert game.renderer is not None, "Where is screen"

    board = game.state.board
    actions = board.get_valid_actions()
    selected = []
    while True:
        print("Waiting player input...")

        # TODO: hightlight pieces with actions
        mouse = game.renderer.mouse_to_grid()

        for action in selected:
            if mouse == action.get_dest():
                game.state.execute(action)
                return

        selected.clear()
        for action in actions:
            if mouse == action.get_piece():
                print(f"Player selected {mouse[0]}, {mouse[1]}")
                selected.append(action)

        print(selected)
        pygame.time.wait(100)
