from abc import ABC, abstractmethod
import random


class HasCoordinates(ABC):
    def __init__(self, tile_width, rect, movement_handler_state=None):
        self.x = 0
        self.y = 0

        self.rect = rect
        self.tile_width = tile_width

        self.movement_handler_state = movement_handler_state

    def set_coordinates(self, new_coordinates):
        self.rect.move_ip((new_coordinates[0] - self.x) * self.tile_width,
                          (new_coordinates[1] - self.y) * self.tile_width)
        self.x, self.y = new_coordinates

    @abstractmethod
    def get_next_turn(self, *args):
        pass


class BaseMovementHandlerState:
    def __init__(self):
        pass

    def __call__(self, direction):
        return direction, self


class ConfusedMovementHandlerStateDecorator:
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
