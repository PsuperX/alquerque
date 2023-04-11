from dataclasses import dataclass
import time
import random

import pygame
from eval_fncs import eval_1
from state import State
from typing import Callable
from typing_extensions import Self
from board import Board, Eat
from gui import Renderer


@dataclass
class Game:
    """
    Holds the game settings
    PlayerX_AI are functions that must return whether or not they changed the state
    """

    state: State
    player1_AI: Callable[[Self], bool]
    player2_AI: Callable[[Self], bool]
    renderer: Renderer | None = None

    def start(self, log_mov=False) -> int:
        """
        Start a new game
        """
        self.state = State(Board(self.state.board.num_rows, self.state.board.num_cols))

        result = -1
        while True:
            if self.state.board.next_player == 1:
                did_action = self.player1_AI(self)
            else:
                did_action = self.player2_AI(self)

            if self.renderer:
                self.renderer.render(self.state)

            if not did_action:
                continue

            if log_mov:
                print(self.state.board)

            result = self.state.board.is_terminal()
            if result != 0:
                break

            if self.renderer:
                pygame.time.wait(500)

        if result == 3:
            print("Nobothy wins :/")
        else:
            print(f"Player {result} Wins :D")

        return result

    def run_n_matches(self, n: int, max_time: int = 3600, log_moves: bool = False):
        """
        utility function to automate n matches execution
        returns the total distribution of players wins and draws
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


def execute_random_move(game: Game) -> bool:
    move = random.choice(game.state.board.get_valid_actions())
    game.state.execute(move)
    return True


def execute_minimax_move(
    evaluate_func: Callable[[State], float], depth: int
) -> Callable[[Game], bool]:
    def execute_minimax_move_aux(game: Game) -> bool:
        """
        updates the game state to the best possible move (uses minimax to determine it)
        """
        best_moves = []
        best_eval = float("-inf")
        actions = game.state.board.get_valid_actions()
        if len(actions) == 1:
            # There isn't much to do and this can take a longggggg time
            game.state.execute(actions[0])
            return True

        player = game.state.board.next_player
        for move in actions:
            game.state.execute(move)
            new_state_eval = minimax(
                game.state,
                depth - 1,
                float("-inf"),
                float("+inf"),
                False,
                player,
                evaluate_func,
            )
            game.state.undo()
            if new_state_eval > best_eval:
                best_moves = [move]
                best_eval = new_state_eval
            elif new_state_eval == best_eval:
                best_moves.append(move)

        assert len(best_moves) != 0, f"Board has no valid actions {game.state.board}"
        game.state.execute(random.choice(best_moves))
        return True

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
        print(evaluate_func(state) * (1 if player == 1 else -1))
        print(state.board, player)
        return evaluate_func(state) * (1 if player == 1 else -1)

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


def execute_player_move(game: Game) -> bool:
    """
    Execute a human move
    """
    assert game.renderer is not None, "Where is screen"

    board = game.state.board
    renderer = game.renderer
    actions = board.get_valid_actions()
    renderer.actions = actions

    if mouse := game.renderer.mouse_to_grid():
        # Undo button
        if mouse == (0, game.state.board.num_rows + 1):
            print("Undo")
            cur_player = game.state.board.next_player
            game.state.undo()
            while game.state.board.next_player != cur_player:
                if not game.state.undo():
                    return True
            renderer.actions = []
            renderer.selected = []
            return True

        # Hint button
        if mouse == (game.state.board.num_cols - 1, game.state.board.num_rows + 1):
            print("Hint")
            execute_minimax_move(eval_1, 6)(game)
            renderer.actions = []
            renderer.selected = []
            return True

        for action in renderer.selected:
            if mouse == action.get_dest():
                game.state.execute(action)
                if isinstance(action, Eat) and not action.changed_turn:
                    actions = board.get_valid_actions()
                    break
                renderer.actions = []
                renderer.selected = []
                return True

        renderer.selected.clear()
        for action in actions:
            if mouse == action.get_piece():
                print(f"Player selected {mouse[0]}, {mouse[1]}")
                renderer.selected.append(action)

    return False
