from typing import List, Tuple
import pygame
from board import Action
from loader import Loader
from state import State


CELL_SIZE = 100
BORDER = (CELL_SIZE, CELL_SIZE)
DOT_SIZE = int(CELL_SIZE // 3)
PIECE_SIZE = int(CELL_SIZE * 0.85)

BOARD_COLOR = 0xDCE1E7
LINE_COLOR = 0x434A5F


class Renderer:
    """
    Responsable for rendering the board using pygame
    """

    width: int
    height: int
    scroll: float
    screen: pygame.Surface
    font: pygame.font.Font
    clock: pygame.time.Clock

    actions: List[Action] = []
    selected: List[Action] = []
    button_held: bool = False

    def __init__(self, num_rows, num_cols):
        self.width = num_cols * CELL_SIZE + BORDER[0] * 2
        self.height = (num_rows + 1) * CELL_SIZE + BORDER[1] * 3

        pygame.init()  # init the game
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # create screen with a certain size
        pygame.display.set_caption("Alquercas")  # display game name
        self.font = pygame.font.SysFont("Arial", 80)
        self.clock = pygame.time.Clock()  # start clock
        self.scroll = 0

    def render(self, state: State):
        """
        Render a frame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.draw_background_with_scroll()
        self.draw_board(state)
        self.draw_pieces(state)
        self.draw_actions()
        self.draw_selected()

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

    def draw_actions(self):
        """
        Draws actions highlights
        """
        highlight = Loader.get_action_image()
        highlight = pygame.transform.scale(highlight, (PIECE_SIZE, PIECE_SIZE))
        for action in self.actions:
            self.screen.blit(
                highlight,
                (
                    BORDER[0]
                    + int(action.get_piece()[0] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - PIECE_SIZE // 2,
                    BORDER[1]
                    + int(action.get_piece()[1] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - PIECE_SIZE // 2,
                ),
            )

    def draw_selected(self):
        """
        Draws selection highlights
        """
        highlight = Loader.get_highlight_image()
        highlight = pygame.transform.scale(highlight, (PIECE_SIZE, PIECE_SIZE))
        for action in self.selected:
            self.screen.blit(
                highlight,
                (
                    BORDER[0]
                    + int(action.get_piece()[0] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - PIECE_SIZE // 2,
                    BORDER[1]
                    + int(action.get_piece()[1] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - PIECE_SIZE // 2,
                ),
            )

        marker = Loader.get_marker_image()
        marker = pygame.transform.scale(marker, (DOT_SIZE, DOT_SIZE))
        for action in self.selected:
            self.screen.blit(
                marker,
                (
                    BORDER[0]
                    + int(action.get_dest()[0] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - DOT_SIZE // 2,
                    BORDER[1]
                    + int(action.get_dest()[1] * CELL_SIZE)
                    + CELL_SIZE // 2
                    - DOT_SIZE // 2,
                ),
            )

    def draw_pieces(self, state: State) -> None:
        """
        Draws player pieces
        """
        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                n = state.board.get_piece(col, row)
                if n == 0:
                    continue

                player = Loader.get_player_image(n)
                player = pygame.transform.scale(player, (PIECE_SIZE, PIECE_SIZE))

                self.screen.blit(
                    player,
                    (
                        BORDER[0]
                        + int(col * CELL_SIZE)
                        + CELL_SIZE // 2
                        - PIECE_SIZE // 2,
                        BORDER[1]
                        + int(row * CELL_SIZE)
                        + CELL_SIZE // 2
                        - PIECE_SIZE // 2,
                    ),
                )

    def draw_board(self, state: State) -> None:
        """
        Draws the board background and lines
        """
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

        dot = Loader.get_dot_image()
        dot = pygame.transform.scale(dot, (DOT_SIZE, DOT_SIZE))
        for row in range(state.board.num_rows):
            for col in range(state.board.num_cols):
                self.screen.blit(
                    dot,
                    (
                        BORDER[0]
                        + int(col * CELL_SIZE)
                        + CELL_SIZE // 2
                        - DOT_SIZE // 2,
                        BORDER[1]
                        + int(row * CELL_SIZE)
                        + CELL_SIZE // 2
                        - DOT_SIZE // 2,
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
        """
        Draws the background texture scrolling
        """
        self.scroll -= 0.5

        if self.scroll < -80:
            self.scroll = 0

        background = Loader.get_background_image()
        self.screen.blit(background, (0, self.scroll))

    def mouse_to_grid(self) -> Tuple[int, int] | None:
        """
        Returns the position of the mouse in grid space if mouse pressed otherwise returns None
        """
        if not pygame.mouse.get_pressed()[0]:
            self.button_held = False
            return None

        if self.button_held:
            return None

        self.button_held = True

        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0] - BORDER[0], mouse[1] - BORDER[1])

        x = mouse[0] // CELL_SIZE
        y = mouse[1] // CELL_SIZE
        return (x, y)
