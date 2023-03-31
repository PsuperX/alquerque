from typing import Tuple
import pygame
from state import State


CELL_SIZE = 100

PLAYER_1_COLOR = (255, 0, 95)  # red
PLAYER_2_COLOR = (125, 205, 0)  # greenish?
EMPTY_CELL_COLOR = (255, 255, 255)  # white
BOARD_COLOR = (0, 0, 0)  # RGB puerple?


class Renderer:
    width: int
    height: int
    screen: pygame.Surface
    font: pygame.font.Font
    clock: pygame.time.Clock

    def __init__(self, num_rows, num_cols):
        self.width = num_cols * CELL_SIZE
        self.height = (num_rows + 1) * CELL_SIZE

        pygame.init()  # init the game
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # create screen with a certain size
        pygame.display.set_caption("Alquercas")  # display game name
        self.font = pygame.font.SysFont("Arial", 80)
        self.clock = pygame.time.Clock()  # start clock

    def render(self, state: State):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.draw_background(state)

        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                color = EMPTY_CELL_COLOR  # if no player played in the circle, fill it with the empty cell color
                if state.board.get_piece(col, row) == 1:
                    color = PLAYER_1_COLOR  # player 1 already played here
                elif state.board.get_piece(col, row) == 2:
                    color = PLAYER_2_COLOR  # player 2 already played here
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        int(col * CELL_SIZE + CELL_SIZE / 2),
                        int(row * CELL_SIZE + CELL_SIZE / 2),
                    ),
                    int(CELL_SIZE / 2.2),
                )

        pygame.display.flip()  # show the board
        self.clock.tick(60)
        pygame.time.wait(500)

    def draw_background(self, state: State) -> None:
        self.screen.fill(BOARD_COLOR)

        # Horizontal
        for row in range(state.board.num_rows):
            start = (
                int(CELL_SIZE / 2),
                int(row * CELL_SIZE + CELL_SIZE / 2),
            )
            end = (
                int(state.board.num_cols * CELL_SIZE - CELL_SIZE / 2),
                int(row * CELL_SIZE + CELL_SIZE / 2),
            )
            pygame.draw.line(self.screen, "white", start, end, 5)

        # Vertical
        for col in range(state.board.num_cols):
            start = (
                int(col * CELL_SIZE + CELL_SIZE / 2),
                int(CELL_SIZE / 2),
            )
            end = (
                int(col * CELL_SIZE + CELL_SIZE / 2),
                int(state.board.num_rows * CELL_SIZE - CELL_SIZE / 2),
            )
            pygame.draw.line(self.screen, "white", start, end, 5)

        # Diagonal
        for row in range(state.board.num_rows - 1):
            for col in range(row % 2, state.board.num_cols - 1, 2):
                start = (
                    int(col * CELL_SIZE + CELL_SIZE / 2),
                    int(row * CELL_SIZE + CELL_SIZE / 2),
                )
                end = (
                    int((col + 1) * CELL_SIZE + CELL_SIZE / 2),
                    int((row + 1) * CELL_SIZE + CELL_SIZE / 2),
                )
                pygame.draw.line(self.screen, "white", start, end, 5)

        for row in range(state.board.num_rows - 1):
            for col in range(2 - row % 2, state.board.num_cols, 2):
                start = (
                    int(col * CELL_SIZE + CELL_SIZE / 2),
                    int(row * CELL_SIZE + CELL_SIZE / 2),
                )
                end = (
                    int((col - 1) * CELL_SIZE + CELL_SIZE / 2),
                    int((row + 1) * CELL_SIZE + CELL_SIZE / 2),
                )
                pygame.draw.line(self.screen, "white", start, end, 5)

    def mouse_to_grid(self) -> Tuple[int, int]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        while not pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.clock.tick(60)
            pygame.time.wait(100)

        mouse = pygame.mouse.get_pos()

        x = mouse[0] // CELL_SIZE
        y = mouse[1] // CELL_SIZE
        return (x, y)
