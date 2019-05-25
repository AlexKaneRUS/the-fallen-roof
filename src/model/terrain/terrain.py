import pygame
from abc import ABC, abstractmethod
from src.util.config import tile_width
from src.model.has_image import HasImage


class Terrain(HasImage, ABC):
    def __init__(self, x, y, image=None, color=(255, 255, 255)):
        self.color = color
        HasImage.__init__(self, topleft=(x * tile_width, y * tile_width))

    def generate_image(self):
        image = pygame.Surface((tile_width, tile_width))
        image.fill(self.color)
        return image


    @abstractmethod
    def isPassable(self):
        pass
