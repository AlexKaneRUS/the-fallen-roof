import pygame
from abc import ABC, abstractmethod
from src.util.config import tile_width


class Terrain(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, image=None, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x * tile_width, y * tile_width))

    @abstractmethod
    def isPassable(self):
        pass
