import pygame
from board import Board
from state import State


CELL_SIZE = 100

PLAYER_1_COLOR = (255, 0, 95)  # red
PLAYER_2_COLOR = (125, 205, 0)  # greenish?
EMPTY_CELL_COLOR = (255, 255, 255)  # white
BOARD_COLOR = (0, 0, 0)  # RGB puerple?


class Renderer:
    def __init__(self, num_cols, num_rows):
        self.width = num_cols * CELL_SIZE
        self.height = (num_rows + 1) * CELL_SIZE

        pygame.init()  # init the game
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # create screen with a certain size
        pygame.display.set_caption("Alquercas")  # display game name
        self.font = pygame.font.SysFont("Arial", 80)
        self.clock = pygame.time.Clock()  # start clock
        # (relevant for AIs to spend some time before moves so that we can visualize)

    def render(self, state: State):
        self.screen.fill(BOARD_COLOR)

        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                color = EMPTY_CELL_COLOR  # if no player played in the circle, fill it with the empty cell color
                if state.board.get_piece(row, col) == 1:
                    color = PLAYER_1_COLOR  # player 1 already played here
                elif state.board.get_piece(row, col) == 2:
                    color = PLAYER_2_COLOR  # player 2 already played here
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        int(col * CELL_SIZE + CELL_SIZE / 2),
                        int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2),
                    ),
                    int(CELL_SIZE / 2.2),
                )

        pygame.display.flip()  # show the board
        self.clock.tick(60)
        pygame.time.wait(500)
