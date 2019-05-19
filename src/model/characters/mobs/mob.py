import random

import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.has_coordinates import HasCoordinates, \
    ConfusedMovementHandlerStateDecorator
from src.model.characters.mobs.strategy import AggressiveStrategy, \
    FrightenedStrategy, PassiveStrategy
from src.util.config import tile_width
from src.util.enums import Color


class Mob(HasCoordinates, HasInventory,
          pygame.sprite.Sprite):
    def __init__(self, world_graph, strategy, health, strength,
                 experience_from_killing, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        HasCoordinates.__init__(self, tile_width, self.rect)
        HasInventory.__init__(self, health, strength)

        self.world_graph = world_graph

        self.strategy = strategy
        self.experience_from_killing = experience_from_killing

    def get_next_turn(self, player_coordinates):
        return self.strategy.get_next_move(self.world_graph, (self.x, self.y),
                                           player_coordinates)

    def on_pickup(self):
        new_item_id = len(self.items) - 1
        new_item = self.items[new_item_id]

        for x in self.equipped_items:
            if self.items[x].item_type == new_item.item_type:
                self.unequip_item(x)
                break

        self.equip_item(new_item_id)

    def level_up(self):
        pass

    def attack(self, other):
        if random.randint(0, 5) == 0:
            other.movement_handler_state = \
                ConfusedMovementHandlerStateDecorator(
                    other.movement_handler_state,
                    3
                )


class MobFactory:
    @staticmethod
    def create_aggressive_mob(world_graph):
        return Mob(world_graph, AggressiveStrategy(), 10, 5, 10,
                   Color.RED.value)

    @staticmethod
    def create_frightened_mob(world_graph):
        return Mob(world_graph, FrightenedStrategy(), 5, 100, 100,
                   Color.BLUE.value)

    @staticmethod
    def create_passive_mob(world_graph):
        return Mob(world_graph, PassiveStrategy(), 100, 0, 0,
                   Color.BROWN.value)

    @staticmethod
    def create_random_mobs(world_graph, n=1):
        return [random.choice([MobFactory.create_aggressive_mob,
                               MobFactory.create_frightened_mob,
                               MobFactory.create_passive_mob])(world_graph) for
                _
                in range(n)]
