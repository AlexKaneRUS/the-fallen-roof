import pygame
from abc import ABC, abstractmethod
from src.util.config import TILE_WIDTH
from src.model.has_image import HasImage


class Terrain(HasImage, ABC):
    def __init__(self, x, y, image=None, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        HasImage.__init__(self)

    def generate_image(self):
        image = pygame.Surface((TILE_WIDTH, TILE_WIDTH))
        image.fill(self.color)
        return image


    @abstractmethod
    def is_passable(self):
        pass
