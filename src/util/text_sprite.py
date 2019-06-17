import pygame
from src.util.enums import Color


class TextSurface:
    @staticmethod
    def get_text_surface(text, font, color=Color.WHITE.value):
        return font.render(text, True, color)
