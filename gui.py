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

jogo = [[0, 0], [0, 0]]


def players_setings(posicao_rato, rec_desejado, jogo, width, height):
    posicaox = 1
    posicaoy = {height * 2 / 5: 1, height * 2 / 5 + 140: 3}
    if rec_desejado.collidepoint(posicao_rato):
        if rec_desejado.midbottom[0] == int(width / 3):
            posicaox = 0
        else:
            posicaox = 1
        jogo[posicaox][0] = posicaoy[rec_desejado.midbottom[1]]
        return True
    return False


def minmaxdif(posicao_rato, rec_das_dif, jogo, width, height):
    posicaox = 1
    posicaoy = {
        height * 2 / 5 + 96: 2,
        height * 2 / 5 + 236: 4,
        height * 2 / 5 + 306: 5,
    }
    if rec_das_dif.collidepoint(posicao_rato):
        if rec_das_dif.midbottom[0] == int(width / 3):
            posicaox = 0
        else:
            posicaox = 1
        jogo[posicaox][0] = posicaoy[rec_das_dif.midbottom[1]]
        celsize = 130 / 18
        jogo[posicaox][1] = int(
            int(int((posicao_rato[0] - rec_das_dif.topleft[0]) / celsize)) / 2 + 2
        )
        return True
    return False


def is_pressede(butt, pos, pressed, jogo):
    if jogo[0][0] != 0 and jogo[1][0] != 0:
        if butt.collidepoint(pos):
            if pressed[0]:
                return True

    return False


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

        self.font1 = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 35)
        self.font3 = pygame.font.Font(None, 25)

    def show_title(self, text: str):
        t = self.font.render(text, True, "black")
        rect = t.get_rect()

        pygame.draw.rect(
            self.screen,
            "grey",
            (
                self.width // 2 - rect.width // 2,
                self.height // 2 - rect.height // 2,
                rect.width,
                rect.height,
            ),
        )
        self.screen.blit(
            t, (self.width // 2 - rect.width // 2, self.height // 2 - rect.height // 2)
        )

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

    def intro_screen(self):
        intro = True

        pygame.display.set_caption("ALQUERQUE")

        textP1 = self.font1.render("P1", True, "olive")
        rec_textP1 = textP1.get_rect(midbottom=(self.width / 3, self.height / 4))
        textP2 = self.font1.render("P2", True, "olive")
        rec_textP2 = textP1.get_rect(midbottom=(self.width * 2 / 3, self.height / 4))

        comecar = self.font1.render("START", True, "olive")
        start = comecar.get_rect(midbottom=(self.width / 2, self.height * 3 / 4 + 81))

        P11 = self.font2.render("random", True, "olive")
        rec_P11 = P11.get_rect(midbottom=(self.width / 3, self.height * 2 / 5))

        P12 = self.font2.render("minimax", True, "olive")
        rec_P12 = P12.get_rect(midbottom=(self.width / 3, self.height * 2 / 5 + 70))
        dif1 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def1 = dif1.get_rect(midbottom=(self.width / 3, self.height * 2 / 5 + 96))
        t1 = False

        P13 = self.font2.render("player", True, "olive")
        rec_P13 = P13.get_rect(midbottom=(self.width / 3, self.height * 2 / 5 + 140))

        P14 = self.font2.render("negamax", True, "olive")
        rec_P14 = P14.get_rect(midbottom=(self.width / 3, self.height * 2 / 5 + 210))
        dif14 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def14 = dif14.get_rect(
            midbottom=(self.width / 3, self.height * 2 / 5 + 236)
        )
        t14 = False

        P15 = self.font2.render("minimax_tt", True, "olive")
        rec_P15 = P15.get_rect(midbottom=(self.width / 3, self.height * 2 / 5 + 280))
        dif15 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def15 = dif15.get_rect(
            midbottom=(self.width / 3, self.height * 2 / 5 + 306)
        )
        t15 = False

        P21 = self.font2.render("random", True, "olive")
        rec_P21 = P21.get_rect(midbottom=(self.width * 2 / 3, self.height * 2 / 5))

        P22 = self.font2.render("minimax", True, "olive")
        rec_P22 = P12.get_rect(midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 70))
        dif2 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def2 = dif2.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 96)
        )
        t2 = False

        P23 = self.font2.render("player", True, "olive")
        rec_P23 = P13.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 140)
        )

        P24 = self.font2.render("negamax", True, "olive")
        rec_P24 = P24.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 210)
        )
        dif24 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def24 = dif24.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 236)
        )
        t24 = False

        P25 = self.font2.render("minimax_tt", True, "olive")
        rec_P25 = P25.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 280)
        )
        dif25 = self.font3.render("2 3 4 5 6 7 8 9 10", True, "olive")
        rec_def25 = dif25.get_rect(
            midbottom=(self.width * 2 / 3, self.height * 2 / 5 + 306)
        )
        t25 = False

        op_diretas = (rec_P11, rec_P13, rec_P21, rec_P23)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if is_pressede(start, mouse_pos, mouse_pressed, jogo):
                intro = False

            self.screen.blit(Loader.get_intro_background_image(), (0, 0))

            self.screen.blit(textP1, rec_textP1)
            self.screen.blit(textP2, rec_textP2)

            self.screen.blit(P11, rec_P11)
            self.screen.blit(P12, rec_P12)
            self.screen.blit(P13, rec_P13)
            self.screen.blit(P14, rec_P14)
            self.screen.blit(P15, rec_P15)

            self.screen.blit(P21, rec_P21)
            self.screen.blit(P22, rec_P22)
            self.screen.blit(P23, rec_P23)
            self.screen.blit(P24, rec_P24)
            self.screen.blit(P25, rec_P25)

            if mouse_pressed[0]:
                print(mouse_pos)

                if mouse_pressed[0]:
                    print(mouse_pos)

                    if rec_P12.collidepoint(mouse_pos):
                        t1 = True
                        t2 = t14 = t15 = t24 = t25 = False
                    elif rec_P22.collidepoint(mouse_pos):
                        t2 = True
                        t1 = t14 = t15 = t24 = t25 = False
                    elif rec_P14.collidepoint(mouse_pos):
                        t14 = True
                        t1 = t2 = t15 = t24 = t25 = False
                    elif rec_P15.collidepoint(mouse_pos):
                        t15 = True
                        t1 = t14 = t2 = t24 = t25 = False
                    elif rec_P24.collidepoint(mouse_pos):
                        t24 = True
                        t1 = t14 = t2 = t15 = t25 = False
                    elif rec_P25.collidepoint(mouse_pos):
                        t25 = True
                        t1 = t14 = t2 = t24 = t15 = False
                    elif t1 and rec_def1.collidepoint(mouse_pos):
                        minmaxdif(
                            mouse_pos, rec_def1, jogo, self.width, self.height
                        )  # escolher dif
                    elif t2 and rec_def2.collidepoint(mouse_pos):
                        minmaxdif(mouse_pos, rec_def2, jogo, self.width, self.height)
                    elif t14 and rec_def14.collidepoint(mouse_pos):
                        minmaxdif(mouse_pos, rec_def14, jogo, self.width, self.height)
                    elif t15 and rec_def15.collidepoint(mouse_pos):
                        minmaxdif(mouse_pos, rec_def15, jogo, self.width, self.height)
                    elif t24 and rec_def24.collidepoint(mouse_pos):
                        minmaxdif(mouse_pos, rec_def24, jogo, self.width, self.height)
                    elif t25 and rec_def25.collidepoint(mouse_pos):
                        minmaxdif(mouse_pos, rec_def25, jogo, self.width, self.height)
                    else:
                        t1 = t2 = t14 = t15 = t24 = t25 = False

                        for membro in op_diretas:
                            players_setings(
                                mouse_pos, membro, jogo, self.width, self.height
                            )

                print(jogo)

                pygame.time.wait(120)

            if t1:
                self.screen.blit(dif1, rec_def1)
            if t2:
                self.screen.blit(dif2, rec_def2)
            if t14:
                self.screen.blit(dif14, rec_def14)
            if t15:
                self.screen.blit(dif15, rec_def15)
            if t24:
                self.screen.blit(dif24, rec_def24)
            if t25:
                self.screen.blit(dif25, rec_def25)

            if jogo[0][0] != 0 and jogo[1][0] != 0:
                self.screen.blit(comecar, start)
            ###############################################

            self.clock.tick(60)
            pygame.display.update()
