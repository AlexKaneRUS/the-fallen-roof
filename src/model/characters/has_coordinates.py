from abc import ABC, abstractmethod
import random


class HasCoordinates(ABC):
    """
    Object that inherits HasCoordinates can be moved in the game.
    """

    def __init__(self, tile_width, rect, movement_handler_state=None):
        """
        :param tile_width: Width of ine tile on screen.
        :param rect: Object's representation on screen.
        :param movement_handler_state: Movement handler that is used to change
        movement logic of an object.
        """
        self.x = 0
        self.y = 0

        self.rect = rect
        self.tile_width = tile_width

        self.movement_handler_state = movement_handler_state

    def set_coordinates(self, new_coordinates):
        """
        Set coordinates of this object to new_coordinates.

        :param new_coordinates: Coordinates to which object is moved.
        :return: None.
        """

        self.rect.move_ip((new_coordinates[0] - self.x) * self.tile_width,
                          (new_coordinates[1] - self.y) * self.tile_width)
        self.x, self.y = new_coordinates

    @abstractmethod
    def get_next_turn(self, *args):
        """
        Returns coordinates where object will be placed next turn.

        :param args: Parameters needed to make object's next turn.
        :return: Coordinates where object will be placed next turn.
        """

        pass


class BaseMovementHandlerState:
    """
    Basic movement handler that doesn't affect object's movement.
    """

    def __init__(self):
        pass

    def __call__(self, direction):
        return direction, self


class ConfusedMovementHandlerStateDecorator:
    """
    Decorator for movement handler that chooses random direction for every
    direction where object is determined to go. As the result object is moved
    to one of three possible directions: where it wanted to go, where it wanted
    to go and left, where it wanted to go and right.
    """

    def __init__(self, base, duration):
        self._base = base
        self._duration = duration

    def __call__(self, direction):
        direction, base = self._base(direction)
        if self._duration:
            return (
                direction.turn_clockwise(random.randint(-1, 1)),
                ConfusedMovementHandlerStateDecorator(base, self._duration - 1)
            )
        else:
            return direction, base
