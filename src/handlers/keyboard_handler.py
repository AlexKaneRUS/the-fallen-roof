import pygame
from src.util.enums import Direction, TurnOwner


class KeyboardHandler:
    def __init__(self, move_command, toggle_inventory_command):
        self.key_handlers = {
            pygame.K_DOWN: self._k_down,
            pygame.K_UP: self._k_up,
            pygame.K_LEFT: self._k_left,
            pygame.K_RIGHT: self._k_right,
            pygame.K_i: self._k_i
        }
        self.move_command = move_command
        self.toggle_inventory_command = toggle_inventory_command

    def handle(self, key):
        if key in self.key_handlers:
            return self.key_handlers[key]()
        else:
            return TurnOwner.PLAYER_TURN

    def _k_down(self):
        self.move_command(Direction.DOWN)
        return TurnOwner.AI_TURN

    def _k_up(self):
        self.move_command(Direction.UP)
        return TurnOwner.AI_TURN

    def _k_left(self):
        self.move_command(Direction.LEFT)
        return TurnOwner.AI_TURN

    def _k_right(self):
        self.move_command(Direction.RIGHT)
        return TurnOwner.AI_TURN

    def _k_i(self):
        self.toggle_inventory_command()
        return TurnOwner.PLAYER_TURN
