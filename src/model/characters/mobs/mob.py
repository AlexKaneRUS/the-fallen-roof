import pygame

from src.model.characters.has_battle_system import HasBattleSystem
from src.model.characters.has_coordinates import HasCoordinates
from src.model.characters.mobs.strategy import AggressiveStrategy
from src.util.config import tile_width


class Mob:
    pass


class AlgoSeminarian(Mob, HasBattleSystem, HasCoordinates,
                     pygame.sprite.Sprite):
    def __init__(self, world_graph):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        HasCoordinates.__init__(self, tile_width, self.rect)

        HasBattleSystem.__init__(self, 10, 5)

        self.world_graph = world_graph

        self.health = 10

        self.strategy = AggressiveStrategy

    def get_next_turn(self, player_coordinates):
        return self.strategy.get_next_move(self.world_graph, (self.x, self.y),
                                           player_coordinates)
