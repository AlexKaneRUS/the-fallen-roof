import random

import pygame

from src.model.characters.has_battle_system import HasBattleSystem
from src.model.characters.has_coordinates import HasCoordinates
from src.model.characters.mobs.strategy import AggressiveStrategy, \
    FrightenedStrategy, PassiveStrategy
from src.util.config import tile_width


class Mob(HasBattleSystem, HasCoordinates,
          pygame.sprite.Sprite):
    """
    A class used to represent mob in the game.

    Mob inherits HasBattleSystem, so it can fight with Player.
    Mob inherits HasCoordinates, so it can be moved.
    """

    def __init__(self, world_graph, strategy, health, strength, color):
        """
        :param world_graph: Object that contains placement of object in game.
        :param strategy: Strategy that defines Mob's behaviour.
        :param health: Amount of health that Mob will have.
        :param strength: Amount of damage that Mob can deal to a Player.
        :param color: RGB color that defines Mob's look.
        """

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        HasCoordinates.__init__(self, tile_width, self.rect)
        HasBattleSystem.__init__(self, health, strength)

        self.world_graph = world_graph

        self.strategy = strategy

    def get_next_turn(self, player_coordinates):
        return self.strategy.get_next_move(self.world_graph, (self.x, self.y),
                                           player_coordinates)


class MobFactory:
    """
    Factory that produces different kinds of Mobs.
    """

    @staticmethod
    def create_aggressive_mob(world_graph):
        """
        Method to produce aggressive Mobs.

        :param world_graph: Object that contains placement of object in game.
        :return: Mob that behaves aggressively.
        """

        return Mob(world_graph, AggressiveStrategy(), 10, 5, (255, 0, 0))

    @staticmethod
    def create_frightened_mob(world_graph):
        """
        Method to produce frightened Mobs.

        :param world_graph: Object that contains placement of object in game.
        :return: Mob that behaves cowardly.
        """

        return Mob(world_graph, FrightenedStrategy(), 5, 100, (0, 0, 255))

    @staticmethod
    def create_passive_mob(world_graph):
        """
        Method to produce passive Mobs.

        :param world_graph: Object that contains placement of object in game.
        :return: Mob that behaves passively.
        """

        return Mob(world_graph, PassiveStrategy(), 100, 0, (174, 152, 105))

    @staticmethod
    def create_random_mobs(world_graph, n=1):
        """
        Method to produce any number of Mobs.

        :param world_graph: Object that contains placement of object in game.
        :param n: Number of Mobs to produce.
        :return: List of n randomly generated Mobs.
        """
        return [random.choice([MobFactory.create_aggressive_mob,
                              MobFactory.create_frightened_mob,
                              MobFactory.create_passive_mob])(world_graph) for _
                in range(n)]
