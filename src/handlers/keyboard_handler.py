import pygame
from src.util.enums import Direction, TurnOwner


class KeyboardHandler:
    '''
    Object that handles player's keyboard actions.
    '''
    def __init__(self, world_model):
        """
        :param world_model: WorldModel instance.
        """
        self.world_model = world_model
        self.key_handlers = {
            pygame.K_DOWN  : self._k_down,
            pygame.K_UP    : self._k_up,
            pygame.K_LEFT  : self._k_left,
            pygame.K_RIGHT : self._k_right
        }

    def handle(self, key):
        """
        Calls appropriate handler for certain key.

        :param key: Key pressed.
        :return: TurnOwner object.
        """
        if key in self.key_handlers:
            return self.key_handlers[key]()
        else:
            return TurnOwner.PLAYER_TURN

    def _k_down(self):
        """
        Handles 'down arrow' key.
        :return: TurnOwner object.
        """
        self.world_model.move_player(Direction.DOWN)
        return TurnOwner.AI_TURN

    def _k_up(self):
        """
        Handles 'up arrow' key.
        :return: TurnOwner object.
        """
        self.world_model.move_player(Direction.UP)
        return TurnOwner.AI_TURN

    def _k_left(self):
        """
        Handles 'left arrow' key.
        :return: TurnOwner object.
        """
        self.world_model.move_player(Direction.LEFT)
        return TurnOwner.AI_TURN

    def _k_right(self):
        """
        Handles 'right arrow' key.
        :return: TurnOwner object.
        """
        self.world_model.move_player(Direction.RIGHT)
        return TurnOwner.AI_TURN
