from typing import Tuple
import pygame
from loader import Loader
from state import State


CELL_SIZE = 100
BORDER = (CELL_SIZE, CELL_SIZE)
DOT_SIZE = (int(CELL_SIZE / 3), int(CELL_SIZE / 3))

PLAYER_1_COLOR = (255, 0, 95)  # red
PLAYER_2_COLOR = (125, 205, 0)  # greenish?
EMPTY_CELL_COLOR = (255, 255, 255)  # white
BOARD_COLOR = 0xDCE1E7  # (0, 0, 0)  # RGB puerple?
LINE_COLOR = 0x434A5F


class Renderer:
    width: int
    height: int
    scroll: float
    screen: pygame.Surface
    font: pygame.font.Font
    clock: pygame.time.Clock

    def __init__(self, num_rows, num_cols):
        self.width = num_cols * CELL_SIZE + BORDER[0] * 2
        self.height = (num_rows + 1) * CELL_SIZE + BORDER[1] * 2

        pygame.init()  # init the game
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # create screen with a certain size
        pygame.display.set_caption("Alquercas")  # display game name
        self.font = pygame.font.SysFont("Arial", 80)
        self.clock = pygame.time.Clock()  # start clock
        self.scroll = 0

    def render(self, state: State):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.draw_background_with_scroll()
        self.draw_board(state)

        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                n = state.board.get_piece(col, row)
                if n == 0:
                    continue

                player = Loader.get_player_image(n)
                player = pygame.transform.scale(player, (CELL_SIZE, CELL_SIZE))

                self.screen.blit(
                    player,
                    (
                        BORDER[0] + int(col * CELL_SIZE),
                        BORDER[1] + int(row * CELL_SIZE),
                    ),
                )

        undo = Loader.get_undo_image()
        undo = pygame.transform.scale(undo, (CELL_SIZE, CELL_SIZE))
        self.screen.blit(
            undo,
            (
                BORDER[0],
                BORDER[1] + int((state.board.num_rows + 1) * CELL_SIZE),
            ),
        )

        hint = Loader.get_hint_image()
        hint = pygame.transform.scale(hint, (CELL_SIZE, CELL_SIZE))
        self.screen.blit(
            hint,
            (
                BORDER[0] + int((state.board.num_rows - 1) * CELL_SIZE),
                BORDER[1] + int((state.board.num_rows + 1) * CELL_SIZE),
            ),
        )

        pygame.display.flip()  # show the board
        self.clock.tick(60)

    def draw_board(self, state: State) -> None:
        # self.screen.fill(BOARD_COLOR)
        rect = pygame.Rect(
            BORDER[0] - 50,
            BORDER[1] - 50,
            CELL_SIZE * state.board.num_cols + 100,
            CELL_SIZE * state.board.num_rows + 100,
        )
        pygame.draw.rect(self.screen, BOARD_COLOR, rect)

        rect = pygame.Rect(
            BORDER[0] - 25,
            BORDER[1] - 25,
            CELL_SIZE * state.board.num_cols + 50,
            CELL_SIZE * state.board.num_rows + 50,
        )
        pygame.draw.rect(self.screen, LINE_COLOR, rect, 10)

        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                dot = Loader.get_dot_image()
                dot = pygame.transform.scale(dot, DOT_SIZE)
                self.screen.blit(
                    dot,
                    (
                        BORDER[0]
                        + int(col * CELL_SIZE)
                        + CELL_SIZE // 2
                        - DOT_SIZE[0] // 2,
                        BORDER[1]
                        + int(row * CELL_SIZE)
                        + CELL_SIZE // 2
                        - DOT_SIZE[1] // 2,
                    ),
                )

        # Horizontal
        for row in range(state.board.num_rows):
            start = (
                BORDER[0] + int(CELL_SIZE / 2),
                BORDER[1] + int(row * CELL_SIZE + CELL_SIZE / 2),
            )
            end = (
                BORDER[0] + int(state.board.num_cols * CELL_SIZE - CELL_SIZE / 2),
                BORDER[1] + int(row * CELL_SIZE + CELL_SIZE / 2),
            )
            pygame.draw.line(self.screen, LINE_COLOR, start, end, 5)

        # Vertical
        for col in range(state.board.num_cols):
            start = (
                BORDER[0] + int(col * CELL_SIZE + CELL_SIZE / 2),
                BORDER[1] + int(CELL_SIZE / 2),
            )
            end = (
                BORDER[0] + int(col * CELL_SIZE + CELL_SIZE / 2),
                BORDER[1] + int(state.board.num_rows * CELL_SIZE - CELL_SIZE / 2),
            )
            pygame.draw.line(self.screen, LINE_COLOR, start, end, 5)

        # Diagonal
        for row in range(state.board.num_rows - 1):
            for col in range(row % 2, state.board.num_cols - 1, 2):
                start = (
                    BORDER[0] + int(col * CELL_SIZE + CELL_SIZE / 2),
                    BORDER[1] + int(row * CELL_SIZE + CELL_SIZE / 2),
                )
                end = (
                    BORDER[0] + int((col + 1) * CELL_SIZE + CELL_SIZE / 2),
                    BORDER[1] + int((row + 1) * CELL_SIZE + CELL_SIZE / 2),
                )
                pygame.draw.line(self.screen, LINE_COLOR, start, end, 7)

        for row in range(state.board.num_rows - 1):
            for col in range(2 - row % 2, state.board.num_cols, 2):
                start = (
                    BORDER[0] + int(col * CELL_SIZE + CELL_SIZE / 2),
                    BORDER[1] + int(row * CELL_SIZE + CELL_SIZE / 2),
                )
                end = (
                    BORDER[0] + int((col - 1) * CELL_SIZE + CELL_SIZE / 2),
                    BORDER[1] + int((row + 1) * CELL_SIZE + CELL_SIZE / 2),
                )
                pygame.draw.line(self.screen, LINE_COLOR, start, end, 7)

    def draw_background_with_scroll(self):
        self.scroll -= 0.5

        if self.scroll < -80:
            self.scroll = 0

        background = Loader.get_background_image()
        self.screen.blit(background, (0, self.scroll))

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
        mouse = (mouse[0] - BORDER[0], mouse[1] - BORDER[1])

        x = mouse[0] // CELL_SIZE
        y = mouse[1] // CELL_SIZE
        return (x, y)
