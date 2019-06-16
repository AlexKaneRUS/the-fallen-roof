import pygame
from abc import ABC, abstractmethod
from src.util.config import tile_width


class Terrain(ABC, pygame.sprite.Sprite):
    '''
    Object that represents terrain.
    '''
    def __init__(self, x, y, image=None, color=(255, 255, 255)):
        """
        :param x: x-coordinate.
        :param y: y-coordinate.
        :param image: Image to display.
        :param color: Filling color if image set to None.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x * tile_width, y * tile_width))

    @abstractmethod
    def is_passable(self):
        """
        Checks if specific terrain can be passed by player.
        """
        pass
