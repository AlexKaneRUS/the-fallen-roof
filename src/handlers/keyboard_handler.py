import pygame
from src.util.enums import Direction, TurnOwner


class KeyboardHandler:
    def __init__(self, world_model):
        self.world_model = world_model
        self.key_handlers = {
            pygame.K_DOWN  : self._k_down,
            pygame.K_UP    : self._k_up,
            pygame.K_LEFT  : self._k_left,
            pygame.K_RIGHT : self._k_right
        }

    def handle(self, key):
        return self.key_handlers[key]()

    def _k_down(self):
        self.world_model.move_player(Direction.DOWN)
        return TurnOwner.AI_TURN

    def _k_up(self):
        self.world_model.move_player(Direction.UP)
        return TurnOwner.AI_TURN

    def _k_left(self):
        self.world_model.move_player(Direction.LEFT)
        return TurnOwner.AI_TURN

    def _k_right(self):
        self.world_model.move_player(Direction.RIGHT)
        return TurnOwner.AI_TURN
