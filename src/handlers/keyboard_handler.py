import pygame
from src.util.enums import Direction, TurnOwner


class KeyboardHandler:
    def __init__(self, game):
        self.game = game
        self.world_model = game.world_model
        self.key_handlers = {
            pygame.K_DOWN: self._k_down,
            pygame.K_UP: self._k_up,
            pygame.K_LEFT: self._k_left,
            pygame.K_RIGHT: self._k_right,
            pygame.K_i: self._k_i
        }

    def handle(self, key):
        if key in self.key_handlers:
            return self.key_handlers[key]()
        else:
            return TurnOwner.PLAYER_TURN

    def _k_down(self):
        self.world_model.move_player(Direction.DOWN, self.game.sprites)
        return TurnOwner.AI_TURN

    def _k_up(self):
        self.world_model.move_player(Direction.UP, self.game.sprites)
        return TurnOwner.AI_TURN

    def _k_left(self):
        self.world_model.move_player(Direction.LEFT, self.game.sprites)
        return TurnOwner.AI_TURN

    def _k_right(self):
        self.world_model.move_player(Direction.RIGHT, self.game.sprites)
        return TurnOwner.AI_TURN

    def _k_i(self):
        if self.game.in_inventory:
            self.game.close_inventory()
        else:
            self.game.open_inventory()

        return TurnOwner.PLAYER_TURN
