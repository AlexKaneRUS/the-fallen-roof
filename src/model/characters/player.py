import pygame

from src.model.characters.has_coordinates import HasCoordinates, \
    BaseMovementHandlerState, ConfusedMovementHandlerStateDecorator
from src.model.characters.has_battle_system import HasBattleSystem
from src.util.config import screen_height, screen_width, tile_width
from src.util.singleton import Singleton


class Player(HasCoordinates, HasBattleSystem, pygame.sprite.Sprite,
             metaclass=Singleton):
    def __init__(self, world_graph):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        HasCoordinates.__init__(self, tile_width, self.rect,
                                ConfusedMovementHandlerStateDecorator(
                                    BaseMovementHandlerState(), 10))

        HasBattleSystem.__init__(self, 100, 10)

        self.world_graph = world_graph

    def get_next_turn(self, direction):
        direction, self.movement_handler_state = self.movement_handler_state(
            direction)

        res = [self.x, self.y]

        if direction.contains_down() and self.rect.bottom < screen_height:
            res[1] += 1
        if direction.contains_up() and self.rect.top > 0:
            res[1] -= 1
        if direction.contains_left() and self.rect.left > 0:
            res[0] -= 1
        if direction.contains_right() and self.rect.right < screen_width:
            res[0] += 1

        res = (res[0], res[1])

        if res in self.world_graph.keys():
            return res
        else:
            return self.x, self.y
