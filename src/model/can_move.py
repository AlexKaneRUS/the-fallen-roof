from abc import ABC, abstractmethod
import random


class CanMove(ABC):
    def __init__(self, movement_handler_state=None, x=0, y=0):
        self.x = x
        self.y = y
        self.movement_handler_state = movement_handler_state

    def get_position(self):
        return (self.x, self.y)


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
