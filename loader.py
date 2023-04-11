import pygame

from paths import ASSETS_DIR, MENU_DIR


class Loader:
    """
    Helper class to load resources
    """

    @staticmethod
    def get_player_image(n: int):
        return pygame.image.load(ASSETS_DIR / f"player{n}.png").convert_alpha()

    @staticmethod
    def get_background_image():
        return pygame.image.load(ASSETS_DIR / "bg.png").convert_alpha()

    @staticmethod
    def get_dot_image():
        return pygame.image.load(ASSETS_DIR / "dot.png").convert_alpha()

    @staticmethod
    def get_undo_image():
        return pygame.image.load(ASSETS_DIR / "undo.png").convert_alpha()

    @staticmethod
    def get_hint_image():
        return pygame.image.load(ASSETS_DIR / "hint.png").convert_alpha()

    @staticmethod
    def get_highlight_image():
        return pygame.image.load(ASSETS_DIR / "highlight.png").convert_alpha()

    @staticmethod
    def get_marker_image():
        return pygame.image.load(ASSETS_DIR / "marker.png").convert_alpha()

    @staticmethod
    def get_action_image():
        return pygame.image.load(ASSETS_DIR / "action.png").convert_alpha()

    @staticmethod
    def get_font():
        pass
