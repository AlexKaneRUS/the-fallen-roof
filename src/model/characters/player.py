import pygame

from src.model.characters.has_coordinates import HasCoordinates
from src.model.characters.has_battle_system import HasBattleSystem
from src.util.enums import Direction
from src.util.config import screen_height, screen_width, tile_width
from src.util.singleton import Singleton


class Player(HasCoordinates, HasBattleSystem, pygame.sprite.Sprite,
             metaclass=Singleton):
    def __init__(self, world_graph):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        HasCoordinates.__init__(self, tile_width, self.rect)

        HasBattleSystem.__init__(self, 10, 10)

        self.world_graph = world_graph

        # pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER))

    def get_next_turn(self, dir):
        res = None

        if dir == Direction.DOWN and self.rect.bottom < screen_height:
            res = (self.x, self.y + 1)
        if dir == Direction.UP and self.rect.top > 0:
            res = (self.x, self.y - 1)
        if dir == Direction.LEFT and self.rect.left > 0:
            res = (self.x - 1, self.y)
        if dir == Direction.RIGHT and self.rect.right < screen_width:
            res = (self.x + 1, self.y)

        if res in self.world_graph.keys():
            return res
        else:
            return self.x, self.y
